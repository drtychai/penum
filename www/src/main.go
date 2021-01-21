// frontend server managing data I/O with flask API
package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"html/template"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

type Hostnames struct {
	Hosts []string
}

func send(arr Hostnames) {
	url := "http://api-rs:5001"
	fmt.Println("URL:>", url)

	b, err := json.Marshal(arr)
	if err != nil {
		fmt.Println("error:", err)
	}
	os.Stdout.Write(b)

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(b))
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	fmt.Println("response Status:", resp.Status)
	fmt.Println("response Headers:", resp.Header)
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("response Body:", string(body))
	return
}

func main() {
	tmpl := template.Must(template.ParseFiles("form.html"))
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			tmpl.Execute(w, nil)
			return
		}
		m := Hostnames{
			Hosts: []string{r.FormValue("hostname")},
		}
		send(m)
	})

	http.HandleFunc("/upload", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			tmpl.Execute(w, nil)
			return
		}
		r.ParseMultipartForm(32 << 20)
		file, _, err := r.FormFile("uploadedfile")
		if err != nil {
			fmt.Println(err)
			return
		}
		defer file.Close()

		// Copy uploaded file to []Bytes
		buf := bytes.NewBuffer(nil)
		_, io_err := io.Copy(buf, file)
		if io_err != nil {
			return
		}

		// Iterate over and append each element to Hostnames struct
		var m Hostnames
		f := buf.String()
		scanner := bufio.NewScanner(strings.NewReader(f))
		for scanner.Scan() {
			m.Hosts = append(m.Hosts, scanner.Text())
		}
		send(m)
	})

	http.ListenAndServe("0.0.0.0:8080", nil)
}
