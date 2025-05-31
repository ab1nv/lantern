package server

import (
	"fmt"
	"net/http"

	"github.com/ab1nv/lantern/routes"
	"github.com/go-chi/chi/v5"
)

func registerRoutes(r chi.Router, baseDir string) {
	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Abhinav is running fast! Watching directory: %s", baseDir)
	})

	routes.RegisterQuestionRoutes(r)
}
