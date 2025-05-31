// Copyright (C) 2025-present Abhinav Singh
// This program is free software under the GNU AGPLv3.
// See <https://www.gnu.org/licenses/> for details.

package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/ab1nv/lantern/config"
	"github.com/ab1nv/lantern/internal/server"
)

func main() {
	// Load config first
	err := config.LoadConfig("lantern-config.json")
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	// Now config.AppConfig is ready to use
	dir := config.AppConfig.GeneralSettings.Directory
	flag.Parse()

	absPath, err := filepath.Abs(dir)
	if err != nil {
		log.Fatalf("Error resolving directory path: %v", err)
	}

	if err := os.MkdirAll(absPath, 0755); err != nil {
		log.Fatalf("Error creating directory: %v", err)
	}

	fmt.Printf("Using directory: %s\n", absPath)

	server.Start(absPath)
}
