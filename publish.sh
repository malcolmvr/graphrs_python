echo "\n\nFirst, set the new version number in pyproject.toml and Cargo.toml."

printf "%s " "When you've set the version numbers, press enter to continue."
read ans

python3 -m pip install --upgrade build
python3 -m build
rm ./dist/graphrs_python-*.whl

echo "\n\nNext, commit and push the code changes to trigger the GitHub cibuildwheels workflow."
echo "Wait for the workflow to complete. Then download the artifacts from the workflow run."
echo "This is done by clicking on each item in the "Matrix: build_wheels" list, then"
echo "clicking on the "Run actions/upload-artifact" step, and finally clicking on the"
echo "artifact download URL. Save each artifact to the dist/ directory.\n"

printf "%s " "When all the wheels have been downloaded, press enter to continue."
read ans

python3 -m pip install --upgrade twine
python3 -m twine upload dist/*