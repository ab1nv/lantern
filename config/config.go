package config

import (
	"encoding/json"
	"fmt"
	"os"
)

type Config struct {
	BuildSettings struct {
		BackendPort  int `json:"BACKEND_PORT"`
		FrontendPort int `json:"FRONTEND_PORT"`
	} `json:"BUILD_SETTINGS"`

	GeneralSettings struct {
		Language  string `json:"LANGUAGE"`
		Theme     string `json:"THEME"`
		Directory string `json:"DIRECTORY"`
	} `json:"GENERAL_SETTINGS"`

	LeetCodeSettings struct {
		Name string `json:"NAME"`
	} `json:"LEETCODE_SETTINGS"`

	CodeforcesSettings struct {
		Name string `json:"NAME"`
	} `json:"CODEFORCES_SETTINGS"`
}

var AppConfig Config

func LoadConfig(path string) error {
	file, err := os.Open(path)
	if err != nil {
		return fmt.Errorf("failed to open config file: %w", err)
	}
	defer file.Close()

	decoder := json.NewDecoder(file)
	if err := decoder.Decode(&AppConfig); err != nil {
		return fmt.Errorf("failed to parse config file: %w", err)
	}

	return nil
}
