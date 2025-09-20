echo %1
d:
cd D:\Analyzer\SourceAnalyzer
git add .
git commit -m %1
git push -u origin main
pause