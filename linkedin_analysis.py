import pandas as pd
import difflib as dfl
import click
import random
import datetime
import moment

common_companies = ['Self Employed', 'Amazon Web Services']
common_positions = {
    'Chief Executive Officer': 'CEO',
    'CEO': 'CEO',
    'Co-Founder & CEO': 'CEO',
    'CEO & Founder': 'CEO',
    'Vice President': 'VP'
}

def getPositionMatch(position):
    #for p in common_positions.keys:
    matches = dfl.get_close_matches(position, common_positions.keys(), 1)
    if len(matches) > 0:
        return common_positions[matches[0]]
    return position

def getCompanyMatch(company):
    #for c in common_companies:
    matches = dfl.get_close_matches(company, common_companies, 1)
    if len(matches) > 0:
        return matches[0]
    return company

def closeMatches(df, row, fieldName, matchFunction):
    #print("\n\n====")
    #print(row)
    # if not df.iloc[row]: return "No Company"
    c1 = str(df.iloc[row][fieldName])
    if not c1: return "None"
    #print(c1)
    return matchFunction(c1)

def summarizeByField(df, fieldName, matchFunction):
    print(matchFunction("self-employed"))
    g = df.groupby(lambda row: closeMatches(df, row, fieldName, matchFunction))
    gSorted = g.size().sort_values(ascending=False)
    print("\n==== SUMMARY ===")
    print(gSorted.head(50))
    #return
    for i in range(0,50):
        fieldValue = gSorted.index[i]
        size = gSorted[i]
        peopleList = g.indices[fieldValue]
        print (fieldValue, " :: ", size)
        #print (peopleList)
        randomPeople = random.sample(list(peopleList), min(5, size))
        for j in randomPeople:
            randomPerson = df.iloc[j]
            print("  ", randomPerson['First Name'], randomPerson['Last Name'], " (", \
                randomPerson['Position'], ", ", randomPerson['Company'], ")")

def messagesOld(mdf):

    #print(mdf)
    mdf['OTHER'] = mdf.apply(lambda x: x['TO'] if x['FROM'] == 'Krishna Mehra' else x['FROM'], axis=1)
    filteredStart = mdf[mdf['DATETIME'] < pd.to_datetime(moment.date("1 year ago").date)]
    filteredByDate = filteredStart[filteredStart['DATETIME'] > pd.to_datetime(moment.date("2 years ago").date)]
    fileredByFolder = filteredByDate[filteredByDate['FOLDER'] == 'INBOX']
    groupedConversations = filteredByDate.groupby('OTHER')
    #multipleConversations = groupedConversations.filter(lambda x: len(x) > 1)
    #print(multipleConversations)
    #sampleConversations = multipleConversations.sample(frac=0.1)

    for key, conversations in groupedConversations.groups.items():
        if len(conversations) <2:
            continue
        sent = 0
        for c in conversations:
            if mdf.iloc[c]['FROM'] == 'Krishna Mehra':
                sent = sent + 1
        if sent == 0:
            continue
        if random.random() > 0.1:
            continue
        print("\n===\n{}\n===".format(key))

        for c in conversations:
            print("  [{}] {}".format(mdf.iloc[c]['DATETIME'], mdf.iloc[c]['CONTENT']))
    return


@click.command()
@click.option('--linkedindir', default="exported", help='Folder where the LinkedIn Data is unzipped')
@click.option('--company/--no-company', default=True, help="Print Company Analysis")
@click.option('--position/--no-position', default=True, help="Print Position Analysis")
def linkedinAnalysis(linkedindir, company, position):
    """Analyzes your LinkedIn Data Export to find people you can get in touch with"""
    # execute only if run as a script

    connectionscsv = linkedindir + "/Connections.csv"
    messagescsv = linkedindir + "/Messages.csv"
    print("Reading file... ", connectionscsv)
    df = pd.read_csv(connectionscsv)
    print("done")
    print(df.head())

    print("Reading messages from: ", messagescsv)
    mdf = pd.read_csv(messagescsv)
    mdf['DATETIME'] = pd.to_datetime(mdf['DATE'], format="%Y-%m-%d %H:%M:%S UTC")
    print(mdf.head())
    messagesOld(mdf)
    # Company Summary
    if company:
        summarizeByField(df, 'Company', getCompanyMatch)
    if position:
        summarizeByField(df, 'Position', getPositionMatch)


if __name__ == "__main__":
    linkedinAnalysis()
