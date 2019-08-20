import os
import subprocess
import fileinput

no_of_test_cases = 3
pytest_file_name = "test.py"
previous_version = "0.1.4"
current_version = "0.1.5"
package_folder = "greendeck_proxygrabber"

# subprocess.run(["python " + pytest_file_name + " > pytest.log"])
print("running all test cases .....")
os.system("pytest " + pytest_file_name + " > pytest.log")

f = open('pytest.log')
lines = f.readlines()

if lines[6].split(pytest_file_name)[1].split("[")[0].strip() == "." * no_of_test_cases:
    print("All test cases passed successfully.")

    print("\n changing package version from " + previous_version + " to " + current_version + " .")

    with fileinput.FileInput("setup.py", inplace=True) as file:
        for line in file:
            print(line.replace(previous_version, current_version), end='')

    with fileinput.FileInput(package_folder + "/__init__.py", inplace=True) as file:
        for line in file:
            print(line.replace(previous_version, current_version), end='')

    print("\n deleting existing build files. ")
    os.system("rm -rf dist")
    # os.system("rm -rf "+package_folder+"*")

    print("\n uploading your package to pip repo....")
    os.system("python setup.py sdist")
    os.system("twine upload dist/*")

    print("\n package uploaded successfully")

else:
    print("All test cases didn't pass")
