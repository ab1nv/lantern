package core

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// QuestionMeta contains essential metadata about a question
type QuestionMeta struct {
	QuestionID    string
	QuestionSlug  string
	QuestionTitle string
}

// CreateLeetCodeFiles creates the necessary directory, solution file, and README
func CreateLeetCodeFiles(baseDir string, meta QuestionMeta, ext string) error {
	// Step 1: Ensure baseDir/leetcode exists
	leetcodeDir := filepath.Join(baseDir, "leetcode")
	if err := os.MkdirAll(leetcodeDir, 0755); err != nil {
		return fmt.Errorf("failed to create leetcode dir: %w", err)
	}

	// Step 2: Create question folder e.g., "1-two-sum"
	folderName := fmt.Sprintf("%s-%s", meta.QuestionID, meta.QuestionSlug)
	questionDir := filepath.Join(leetcodeDir, folderName)
	if err := os.MkdirAll(questionDir, 0755); err != nil {
		return fmt.Errorf("failed to create question dir: %w", err)
	}

	// Step 3: Create solution file (if not exists)
	solutionFile := filepath.Join(questionDir, meta.QuestionSlug+ext)
	if _, err := os.Stat(solutionFile); os.IsNotExist(err) {
		if err := os.WriteFile(solutionFile, []byte(""), 0644); err != nil {
			return fmt.Errorf("failed to create solution file: %w", err)
		}
	}

	// Step 4: Create README.md (if not exists)
	readmePath := filepath.Join(questionDir, "README.md")
	if _, err := os.Stat(readmePath); os.IsNotExist(err) {
		content := fmt.Sprintf("# %s\n", strings.TrimSpace(meta.QuestionTitle))
		if err := os.WriteFile(readmePath, []byte(content), 0644); err != nil {
			return fmt.Errorf("failed to write README.md: %w", err)
		}
	}

	return nil
}
