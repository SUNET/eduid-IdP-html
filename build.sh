set -x
set -e

package="eduid-IdP-html"
srcdir="eduid-IdP-html"

git status
ls -l

test "x$package" = "x" && package="$1"
test "x$srcdir" = "x" && srcdir="$2"
test "x$testworkdir" = "x" && testworkdir="$3"
test "x$testworkdir" = "x" && testworkdir="$WORKSPACE"

if [ "x$package" = "x" ]; then
  echo "Missing package argument"
  exit 1
fi

if [ "x$srcdir" = "x" ]; then
  echo "Missing srcdir argument"
  exit 1
fi

cd $WORKSPACE
export VIRTUAL_ENV="$WORKSPACE/venv_${BUILD_NUMBER}"
virtualenv --no-site-packages $VIRTUAL_ENV
export PIP_DOWNLOAD_CACHE=/var/cache/jenkins/pip
export PIP_INDEX_URL=https://pypi.sunet.se/simple/

. $VIRTUAL_ENV/bin/activate

python --version

pip install -U setuptools
pip install -U pip

test -f requirements.txt && pip install --pre -r requirements.txt
test -f test_requirements.txt && pip install --pre --upgrade -r test_requirements.txt
test -f requirements/testing.txt && pip install --pre -r requirements/testing.txt
# only pysaml2 is known to use tests/test_requirements.txt
test -f tests/test_requirements.txt && pip install --pre -r tests/test_requirements.txt

# By white listing pypi.sunet.se and pypi.python.org we forbidd easy_install
# to fetch package from very slow servers like the one from python-dateutil
# Easy_install tries to do that in order to look if there are newer versions
python ./setup.py develop --index-url https://pypi.sunet.se/simple --allow-hosts *.sunet.se,*.python.org,*.pythonhosted.org,*.github.com,*.launchpad.net,*.cherrypy.org,*.sf.net,*.sourceforge.net
# compile language files if project has a 'locale' directory
test -d */locale && python setup.py compile_catalog
test -d */locale && find */locale -type f -ls

####### eduid-IdP specific ##########
# Generate html files for inclusion in the package
python generate-html-files eduid_IdP_html/html
####### eduid-IdP specific ##########

python ./setup.py sdist install
test -f setup.cfg && grep -q testing setup.cfg && python ./setup.py testing

pip install nose nosexcover pylint

# show installed package versions
pip freeze

rm -f nosetests.xml
rm -f */nosetests.xml

cd $WORKSPACE
nosetests --with-xunit --xunit-file=$WORKSPACE/nosetests.xml --with-xcoverage --cover-xml --cover-xml-file=$WORKSPACE/coverage.xml --cover-package=${package} --cover-erase

pylint -f parseable ${package} | tee pylint.out
ls -l pylint.out || true
# eduid-dashboard has strange directory layout... oh my, what a hack.
grep -q "No module named ${package}" pylint.out && pylint -f parseable ${srcdir} | tee pylint.out
sed -i 's%/opt/work/%%' pylint.out

sloccount --duplicates --wide --details ${srcdir} > sloccount.sc

rm -rf $VIRTUAL_ENV
# show files likely to be copied to pypi.sunet.se
echo "Resulting artifacts :"
ls -l dist/*.tar.gz dist/*.egg || ls -l

# for debugging missing coverage data
find . -name coverage.xml -ls
find . -name nosetests.xml -ls


