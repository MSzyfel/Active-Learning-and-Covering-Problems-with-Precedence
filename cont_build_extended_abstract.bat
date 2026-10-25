@echo off
setlocal enabledelayedexpansion

:: Sprawdzenie czy istnieje extended_abstract.tex
IF NOT EXIST extended_abstract.tex (
    echo Plik extended_abstract.tex nie istnieje w tym katalogu!
    exit /b
)

:loop
    echo.
    echo ==============================
    echo Kompilacja pdfLaTeX (1/4)...
    pdflatex -interaction=nonstopmode extended_abstract.tex

    echo Uruchamianie BibTeX (2/4)...
    bibtex extended_abstract

    echo Kompilacja pdfLaTeX (3/4)...
    pdflatex -interaction=nonstopmode extended_abstract.tex

    echo Kompilacja pdfLaTeX (4/4)...
    pdflatex -interaction=nonstopmode extended_abstract.tex

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
