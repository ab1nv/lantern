// Copyright (C) 2025-present Abhinav Singh
// This program is free software under the GNU AGPLv3.
// See <https://www.gnu.org/licenses/> for details.

package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/a-h/templ"
	"github.com/ab1nv/lantern/client/assets"
	"github.com/ab1nv/lantern/client/ui/pages"
	"github.com/ab1nv/lantern/internal/server"
)

func main() {
	dir := flag.String("dir", "problemset", "Directory to watch or create")
	addr := flag.String("addr", ":8080", "HTTP server address")
	flag.Parse()

	absPath, err := filepath.Abs(*dir)
	if err != nil {
		log.Fatalf("Error resolving directory path: %v", err)
	}

	if err := os.MkdirAll(absPath, 0755); err != nil {
		log.Fatalf("Error creating directory: %v", err)
	}

	fmt.Printf("📂 Using problem directory: %s\n", absPath)

	// Start backend processing
	go server.Start(absPath)

	// Set up HTTP routes
	mux := http.NewServeMux()

	// Serve embedded CSS and other assets
	mux.Handle("/assets/", http.StripPrefix("/assets/", http.FileServer(http.FS(assets.Assets))))

	// Serve root landing page via templ
	mux.Handle("/", templ.Handler(pages.Landing()))

	fmt.Printf("🌐 Server running at http://localhost%s\n", *addr)
	if err := http.ListenAndServe(*addr, mux); err != nil {
		log.Fatalf("HTTP server failed: %v", err)
	}
}
