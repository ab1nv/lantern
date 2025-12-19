import tempfile
from pathlib import Path

import pytest

from lantern.filesystem import FileSystemManager


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_initialize_creates_solutions_folder(temp_dir):
    manager = FileSystemManager(temp_dir)
    manager.initialize()
    
    assert manager.solutions_folder.exists()
    assert manager.solutions_folder.name in ["problemset", "solutions"]
    assert manager.readme_path.exists()


def test_ensure_question_folder(temp_dir):
    manager = FileSystemManager(temp_dir)
    manager.initialize()
    
    folder = manager.ensure_question_folder("1", "two-sum")
    assert folder.exists()
    assert folder.name == "0001-two-sum"


def test_ensure_question_readme(temp_dir):
    manager = FileSystemManager(temp_dir)
    manager.initialize()
    
    folder = manager.ensure_question_folder("1", "two-sum")
    problem_data = {
        "question_id": "1",
        "question_title": "Two Sum",
        "question_slug": "two-sum",
        "difficulty": "Easy",
        "topic_tags": "Array, Hash Table",
    }
    
    manager.ensure_question_readme(folder, problem_data)
    
    readme = folder / "README.md"
    assert readme.exists()
    content = readme.read_text()
    assert "Two Sum" in content
    assert "Easy" in content
    assert "Array, Hash Table" in content


def test_ensure_solution_file(temp_dir):
    manager = FileSystemManager(temp_dir)
    manager.initialize()
    
    folder = manager.ensure_question_folder("1", "two-sum")
    manager.ensure_solution_file(folder, "python")
    
    solution_file = folder / "solution.py"
    assert solution_file.exists()


def test_create_table_if_missing(temp_dir):
    manager = FileSystemManager(temp_dir)
    manager.initialize()
    
    manager.create_table_if_missing()
    
    content = manager.readme_path.read_text()
    assert "| # | Title | Solution | Tags | Difficulty |" in content
    assert "|:----:|:--------:|:--------:|:-------:|:----------:|" in content


def test_parse_table_rows(temp_dir):
    manager = FileSystemManager(temp_dir)
    manager.initialize()
    
    content = manager.readme_path.read_text()
    content += "\n| # | Title | Solution | Tags | Difficulty |\n"
    content += "|:----:|:--------:|:--------:|:-------:|:----------:|\n"
    content += "| 0001 | [Two Sum](https://leetcode.com/problems/two-sum/) | [Python](./problemset/0001-two-sum/solution.py) | Array | Easy |\n"
    manager.readme_path.write_text(content)
    
    rows = manager.parse_table_rows()
    assert len(rows) == 1
    assert rows[0]["question_id"] == 1
    assert rows[0]["title"] == "Two Sum"
    assert len(rows[0]["solutions"]) == 1


def test_update_readme_table_new_entry(temp_dir):
    manager = FileSystemManager(temp_dir)
    manager.initialize()
    
    problem_data = {
        "question_id": "1",
        "question_title": "Two Sum",
        "question_slug": "two-sum",
        "difficulty": "Easy",
        "topic_tags": "Array, Hash Table",
    }
    
    manager.ensure_question_folder("1", "two-sum")
    manager.ensure_solution_file(manager.solutions_folder / "0001-two-sum", "python")
    manager.update_readme_table(problem_data, "python")
    
    content = manager.readme_path.read_text()
    assert "0001" in content
    assert "Two Sum" in content
    assert "Easy" in content


def test_update_readme_table_existing_entry(temp_dir):
    manager = FileSystemManager(temp_dir)
    manager.initialize()
    
    problem_data = {
        "question_id": "1",
        "question_title": "Two Sum",
        "question_slug": "two-sum",
        "difficulty": "Easy",
        "topic_tags": "Array, Hash Table",
    }
    
    folder = manager.ensure_question_folder("1", "two-sum")
    manager.ensure_solution_file(folder, "python")
    manager.update_readme_table(problem_data, "python")
    
    manager.ensure_solution_file(folder, "go")
    manager.update_readme_table(problem_data, "go")
    
    rows = manager.parse_table_rows()
    assert len(rows) == 1
    assert len(rows[0]["solutions"]) == 2


def test_update_readme_table_sorts_by_id(temp_dir):
    manager = FileSystemManager(temp_dir)
    manager.initialize()
    
    problem_data1 = {
        "question_id": "233",
        "question_title": "Problem 233",
        "question_slug": "problem-233",
        "difficulty": "Medium",
        "topic_tags": "Tag1",
    }
    
    problem_data2 = {
        "question_id": "3",
        "question_title": "Problem 3",
        "question_slug": "problem-3",
        "difficulty": "Easy",
        "topic_tags": "Tag2",
    }
    
    folder1 = manager.ensure_question_folder("233", "problem-233")
    folder2 = manager.ensure_question_folder("3", "problem-3")
    
    manager.ensure_solution_file(folder1, "python")
    manager.ensure_solution_file(folder2, "python")
    
    manager.update_readme_table(problem_data1, "python")
    manager.update_readme_table(problem_data2, "python")
    
    rows = manager.parse_table_rows()
    assert len(rows) == 2
    assert rows[0]["question_id"] == 3
    assert rows[1]["question_id"] == 233

