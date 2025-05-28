package server

import (
	"fmt"
	"net/http"
)

func registerRoutes(mux *http.ServeMux, baseDir string) {
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Lantern is running! Watching directory: %s", baseDir)
	})
}
