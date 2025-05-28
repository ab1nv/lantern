package server

import (
	"fmt"
	"log"
	"net/http"
)

func Start(baseDir string) {
	mux := http.NewServeMux()
	registerRoutes(mux, baseDir)

	fmt.Println("Server running on http://localhost:8080")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
