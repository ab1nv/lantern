package main

import (
	"log"
	"net/http"

	"github.com/ab1nv/lantern/frontend/pages"

	"github.com/a-h/templ"
)

func main() {
	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("frontend/assets/css/dist"))))
	http.Handle("/", templ.Handler(pages.Index()))

	log.Println("Frontend server running on http://localhost:3000")
	log.Fatal(http.ListenAndServe(":3000", nil))
}
