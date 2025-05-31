package server

import (
	"fmt"
	"log"
	"net/http"

	"github.com/ab1nv/lantern/config"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

func Start(baseDir string) {
	r := chi.NewRouter()
	port := config.AppConfig.BuildSettings.BackendPort
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	registerRoutes(r, baseDir)

	fmt.Printf("Server running on http://localhost:%d\n", port)
	if err := http.ListenAndServe(fmt.Sprintf(":%d", port), r); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
