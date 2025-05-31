package server

import (
	"fmt"
	"net/http"

	routes "github.com/ab1nv/lantern/internal/routes/question"
	"github.com/go-chi/chi/v5"
)

func registerRoutes(r chi.Router, baseDir string) {
	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Abhinav is running fast! Watching directory: %s", baseDir)
	})

	routes.RegisterQuestionRoutes(r)
}
