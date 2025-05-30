package main

import (
	"fmt"
	"net/http"
	"os"

	"github.com/a-h/templ"
	"github.com/ab1nv/lantern/client/assets"
	"github.com/ab1nv/lantern/client/ui/pages"
	"github.com/joho/godotenv"
)

func main() {
	InitDotEnv()
	mux := http.NewServeMux()
	SetupAssetsRoutes(mux)
	mux.Handle("GET /", templ.Handler(pages.Landing()))

	fmt.Println("Server is running on http://localhost:8090")
	http.ListenAndServe(":8090", mux)
}

func InitDotEnv() {
	_ = godotenv.Load()
}

func SetupAssetsRoutes(mux *http.ServeMux) {
	isDev := os.Getenv("GO_ENV") != "production"

	var fs http.Handler
	if isDev {
		fs = http.FileServer(http.Dir("client/assets/css"))
	} else {
		fs = http.FileServer(http.FS(assets.Assets))
	}

	handler := http.StripPrefix("/assets/", fs)

	mux.Handle("/assets/", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if isDev {
			w.Header().Set("Cache-Control", "no-store")
		}
		handler.ServeHTTP(w, r)
	}))
}
