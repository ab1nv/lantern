// Copyright (C) 2025-present Abhinav SinghAdd commentMore actions
// This program is free software under the GNU AGPLv3.
// See <https://www.gnu.org/licenses/> for details.

package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/ab1nv/lantern/internal/server"
)

func main() {
	dir := flag.String("dir", "problemset", "Directory to watch or create")
	flag.Parse()

	absPath, err := filepath.Abs(*dir)
	if err != nil {
		log.Fatalf("Error resolving directory path: %v", err)
	}

	if err := os.MkdirAll(absPath, 0755); err != nil {
		log.Fatalf("Error creating directory: %v", err)
	}

	fmt.Printf("Using directory: %s\n", absPath)

	server.Start(absPath)
}
