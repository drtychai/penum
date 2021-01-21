extern crate dropshot;
extern crate tokio;
extern crate async_std;
extern crate hyper;
extern crate http;
extern crate serde;
extern crate schemars;
extern crate phf;
#[macro_use]
extern crate slog;
extern crate slog_syslog;
extern crate futures;

use crate::tokio::task;
use crate::hyper::{Body, Response};
use crate::http::StatusCode;
use crate::dropshot::{
    endpoint,
    ApiDescription,
    ConfigDropshot,
    ConfigLogging,
    ConfigLoggingLevel,
    ConfigLoggingIfExists,
    TypedBody,
    HttpError,
    HttpServer,
    RequestContext,
};
use crate::schemars::JsonSchema;
use crate::serde::Deserialize;
use ::std::sync::Arc;

mod tools;

/// DNS tools that we'll run asynchronously. The
/// output of these funnel into massDNS.
static DNS_ENUM_TOOLS: &'static [ &'static str ] = &[
    "amass",
    "subfinder", 
    "aiodnsbrute",
    "sublist3r",
    "gobuster",
    "recon-ng",
];

#[allow(non_snake_case)]
#[derive(Clone, Deserialize, JsonSchema)]
struct Config {
    Hosts: Option<Vec<String>>,
}

async fn watchdog(targets: Vec<String>) -> async_std::io::Result<()> {
    let mut trgt_iter = targets.into_iter(); 
    loop {
        let trgt = match trgt_iter.next() {
            Some(t) => t,
            None => break,
        };

        let log = ConfigLogging::File {
            level: ConfigLoggingLevel::Trace,
            path: ::std::env::var("API_RUNTIME_LOG_FILE").unwrap(),
            if_exists: ConfigLoggingIfExists::Append,
        }
        .to_logger(format!("{}", trgt.clone()))
        .map_err(|e| e.to_string()).unwrap();
   
        // Launch a watchdog for each tool/host/port triple
        info!(log, "Starting watchdog for {:?}", trgt.clone());
        let runner = tools::Runner::new(trgt, DNS_ENUM_TOOLS, log);

        let join = task::spawn(async move {
            runner.run().await;
        });

        // Await the result of the spawned task.
        let _ = join.await?;
    }
    Ok(())
}


/// Generic endpoint used for target ingestion and kick-off from www container. Input takes the
/// form of JSON with single "Hosts" key, e.g.: { "Hosts" : ["example.com", "yahoo.com"] }
#[endpoint(method = POST, path = "/")]
async fn configure(_rqctx: Arc<RequestContext>, body_param: TypedBody<Config>) -> Result<Response<Body>, HttpError> {
    let trgts = body_param.into_inner().Hosts.unwrap();
    let _ = watchdog(trgts).await;

    Ok(Response::builder()
        .status(StatusCode::OK)
        .body("".into())?
        )
}

/// HTTP APIs used to initiate and coordinate enumeration tools, their respective
/// containers, and results. 
///
/// 
#[tokio::main]
async fn main() -> Result<(), String> {
    // Set up a logger.
    let log = ConfigLogging::File {
        level: ConfigLoggingLevel::Trace,
        path: ::std::env::var("API_LOG_FILE").unwrap(),
        if_exists: ConfigLoggingIfExists::Append,
    }
    .to_logger("penum")
    .map_err(|e| e.to_string())?;

    // Create an API group and register our routes
    let mut api = ApiDescription::new();
    api.register(configure).unwrap();

    //api.print_openapi(
    //    &mut std::io::stdout(),
    //    &"psv",
    //    None,
    //    None,
    //    None,
    //    None,
    //    None,
    //    None,
    //    None,
    //    &"",
    //)
    //.map_err(|e| e.to_string())?;

    // Start the server.
    let mut server = HttpServer::new(
        &ConfigDropshot {
            bind_address: "0.0.0.0:5001".parse().unwrap(),
        },
        api,
        Arc::new(()),
        &log,
    )
    .map_err(|error| format!("failed to start server: {}", error))?;

    let server_task = server.run();
    server.wait_for_shutdown(server_task).await
}
