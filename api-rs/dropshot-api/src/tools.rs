use crate::async_std::io;
use crate::async_std::net::TcpStream;
use crate::async_std::prelude::*;
use crate::futures::stream::FuturesUnordered;

use crate::slog::Logger;
use crate::phf::{Map, phf_map};

use ::std::collections::HashSet;

/// Static hostname <=> port mapping. Used mostly for lookups.
static TOOL_MAP: Map<&'static str, u32> = phf_map! {
    // DNS
    "amass"       => 30000,
    "subfinder"   => 30001,
    "aiodnsbrute" => 30002,
    "sublist3r"   => 30003,
    "gobuster"    => 30004,
    "massdns"     => 30005,
    "recon-ng"    => 30006,

    // HTTP
    "aquatone"    => 30007,
    "httprobe"    => 30008,
    "wart"        => 30009,
    "nikto"       => 30010,
    "dirsearch"   => 30011,
    "nmap"        => 30012,
    "wafw00f"     => 30013,
};
 
/// Script runner for api-rs. Each runner holds only
/// one target. Multitple runners will be used for 
/// multi-target requests.
#[derive(Debug,Clone)]
pub struct Runner {
    // Host target
    target: String,

    // Tools to execute
    tools: &'static [ &'static str ],

    // This runner's logger
    logger: slog::Logger,

}


impl Runner {
    pub fn new(target: String, tools: &'static [ &'static str ], logger: Logger) -> Self {
        Self { target, tools, logger }
    }

    pub async fn run(&self) -> Vec<Vec<u8>> { 
        let mut tool_iterator = self.tools.clone().into_iter();	

        let mut ftrs = FuturesUnordered::new(); 
        let mut errors: HashSet<String> = HashSet::with_capacity(self.tools.len() * 10);
        let mut tool_output: Vec<Vec<u8>> = Vec::new();

        loop {
            match tool_iterator.next() {
                Some(tool) => ftrs.push(self.run_tool(tool)),
                None => break,
            };
        }

        while let Some(result) = ftrs.next().await {
            match result {
                Ok(out) => tool_output.push(out),
                Err(e) => {
                    let error_string = e.to_string();
                    if errors.len() < self.tools.len() * 10 {
                        errors.insert(error_string);
                    }
                }
            }
        }
        tool_output
    }


    async fn run_tool(&self, tool: &'static str) -> io::Result<Vec<u8>> {
        let uri = format!("{}:{}", tool.clone(), TOOL_MAP[tool]);

        // Kick off tool and wait on async thread
        let mut stream = TcpStream::connect(uri).await?;

        // Launch a watchdog for each tool/host/port triple
        info!(self.logger, "Starting watchdog for {} on {}", self.target.clone(), tool.clone());
        stream.write_all(&self.target.clone().into_bytes());
        
        let mut buf = vec![0u8; 4];
        let join = stream.read(&mut buf);

        debug!(self.logger, "{:?}", join.await?);
        Ok(buf)
    }
}
