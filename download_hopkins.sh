RANDNUM=`date +%s`
TMPDIR=tmpdir${RANDNUM}
DATADIR='data/csse'


# Download using git
mkdir -p ${TMPDIR}
cd ${TMPDIR}
git clone https://github.com/CSSEGISandData/COVID-19.git
cd ../

# Copy to data/
mkdir -p ${DATADIR}
cp -r $TMPDIR/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/* ${DATADIR}

# Cleanup
rm -fr ${TMPDIR}

