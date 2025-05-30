# ---------- CONFIG ----------
FRONTEND_DIR := client
BACKEND_ENTRY := ./cmd/main.go
TMP_BIN := tmp/bin
OUTPUT := $(TMP_BIN)/lantern

# ---------- DEV ----------
dev:
	GO_ENV=development air

# ---------- PRODUCTION BUILD ----------
build:
	@echo "🔧 Generating templ files..."
	cd $(FRONTEND_DIR) && templ generate

	@echo "🎨 Compiling Tailwind CSS..."
	tailwindcss -i $(FRONTEND_DIR)/assets/css/input.css -o $(FRONTEND_DIR)/assets/css/output.css --minify

	@echo "🚀 Building production binary..."
	GO_ENV=production go build -o $(OUTPUT) $(BACKEND_ENTRY)

	@echo "✅ Build complete: $(OUTPUT)"

# ---------- CLEAN ----------
clean:
	rm -rf $(TMP_BIN)
