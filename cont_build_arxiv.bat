@echo off
setlocal enabledelayedexpansion

:: Sprawdzenie czy istnieje main_arxiv.tex
IF NOT EXIST main_arxiv.tex (
    echo Plik main_arxiv.tex nie istnieje w tym katalogu!
    exit /b
)

:loop
    echo.
    echo ==============================
    echo Kompilacja pdfLaTeX (1/4)...
    pdflatex -interaction=nonstopmode main_arxiv.tex

    echo Uruchamianie BibTeX (2/4)...
    bibtex main_arxiv

    echo Kompilacja pdfLaTeX (3/4)...
    pdflatex -interaction=nonstopmode main_arxiv.tex

    echo Kompilacja pdfLaTeX (4/4)...
    pdflatex -interaction=nonstopmode main_arxiv.tex

    echo Kompilacja zakonczona.
    echo ==============================
    echo.

    :: Sprawdź czy user cos kliknął
    choice /c CQ /n /t 0 /d C >nul
    if errorlevel 2 (
        echo Wykryto zadanie zamkniecia. Koniec.
        exit /b
    )

goto loop
