import zipfile
import os
import shutil
import xlrd
import pandas
import psycopg2

def getzipfiles(datadir):
    files =  os.listdir(datadir)
    return [file for file in files if file.endswith('zip')]

def extractzipfile(zippedfiles, dataDir, tmpDir):
    for fl in zippedfiles:
        filepath = os.path.join(dataDir,fl)
        zip_rf = zipfile.ZipFile(filepath, 'r')
        zip_rf.extractall(tmpDir)
        zip_rf.close()

def changedir(tmpDir):
    dirs = [i[0] for i in os.walk(tmpDir)][1:]

    for dir in dirs:
        fls = [i[2] for i in os.walk(dir)][0]

        for fl in fls:
            fl_path = os.path.join(dir, fl)
            new_fl_path = os.path.join(tmpDir, fl)
            shutil.copy(fl_path, new_fl_path)

        shutil.rmtree(dir)

def excel2csv(tmpDir):
    files = [file for file in os.listdir(tmpDir) if 'xls' in file]

    for file in files:
        loadxldata(file, tmpDir)

def loadxldata(file, tmpDir):
    filepath = os.path.join(tmpDir, file)

    xl_workbook = xlrd.open_workbook(filepath)

    for i in range(3):
        xl_sheet = xl_workbook.sheet_by_index(i)

        row1 = xl_sheet.row_values(1)
        exit_ind = [j for j in range(len(row1)) if row1[j] == 'Exits'][0]

        data_sheet = []
        for q in range(exit_ind):
            row = xl_sheet.row_values(q + 1)[:exit_ind]
            data_sheet.append(row)

        stations = [''.join(list(str(val))[:2]) for val in data_sheet[0]]

        for r in range(len(stations)):
            data_sheet[r][0] = stations[r]
            data_sheet[0][r] = stations[r]

        reshapedata(data_sheet,i, stations[1:exit_ind], file, tmpDir)

def reshapedata(data_sheet, i, row1, file, tmpDir):
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September","October", "November", "December"]
    years = range(2001, 2017)
    daytypes = ['Weekday', 'Saturday', 'Sunday']

    data_sheet[0][0] = 'term'
    data_sheet_pd = pandas.DataFrame(data_sheet[1:], columns=data_sheet[0])
    data_sheet_pd = pandas.melt(data_sheet_pd, id_vars='term', value_vars= row1,
                             var_name='start', value_name='riders')

    month = [j+1 for j in range(len(months)) if months[j] in file]
    year = [years[q] for q in range(len(years)) if str(years[q]) in file]
    daytype = daytypes[i]

    data_sheet_pd['mon'] = month * data_sheet_pd.shape[0]
    data_sheet_pd['yr'] = year * data_sheet_pd.shape[0]
    data_sheet_pd['daytype'] = [daytype] * data_sheet_pd.shape[0]

    data_sheet_pd = data_sheet_pd[['mon','yr','daytype','start','term','riders']]

    storecsv(data_sheet_pd, year[0], month[0], daytype, tmpDir)

def storecsv(data_sheet, year, month, daytype, tmpDir):
    filename = str(year)+'_'+str(month)+'_'+daytype+'.csv'
    filepath = os.path.join(tmpDir, filename)
    data_sheet.to_csv(filepath, index=False, header=None)

def runsql(SQLConn, schema, table, tmpDir):

    curr = SQLConn.cursor()
    crt_tbl = """
    DROP TABLE IF EXISTS %s.%s;
    CREATE TABLE %s.%s
    (
    mon int
    , yr int
    , daytype varchar(15)
    , start varchar(2)
    , term varchar(2)
    , riders float
    );""" % (schema, table, schema, table)

    executesql(crt_tbl, curr, SQLConn)

    csvfiles = [file for file in os.listdir(tmpDir) if file.endswith('.csv')]
    [csv2sql(csvfile, schema, table, tmpDir, curr, SQLConn) for csvfile in csvfiles]

def executesql(query, curr, SQLConn):
    try:
        curr.execute(query)
        SQLConn.commit()
    except psycopg2.ProgrammingError:
        print "FAILED :%s" % (query,)
        SQLConn.rollback()

def csv2sql(csvfile, schema, table, tmpdir, curr, SQLConn):
    csvfilepath = os.path.join(tmpdir, csvfile)
    query = "COPY %s.%s FROM '%s' CSV;" % (schema,table, csvfilepath)
    executesql(query, curr, SQLConn)

def processBart(tmpDir, dataDir, SQLConn = None, schema = 'cls', table = 'bart'):

    zippedfiles =  getzipfiles(dataDir)
    extractzipfile(zippedfiles, dataDir, tmpDir)
    changedir(tmpDir)
    excel2csv(tmpDir)
    runsql(SQLConn, schema, table, tmpDir)

SQLConn = psycopg2.connect("dbname='stocks' host='localhost'")
processBart('/Users/nis89mad/Dropbox/MSAN/Fall/SQL/HW3/tmpDir',
            '/Users/nis89mad/Dropbox/MSAN/Fall/SQL/HW3/dataDir', SQLConn=SQLConn)









