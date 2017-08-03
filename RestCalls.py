import tableauserverclient as TSC
import sys

def setDefaultEncoding ():
    reload(sys)
    sys.setdefaultencoding('windows-1250')
    return

def setPagination ():
    return TSC.RequestOptions(pagesize=1000)

def stripCharacter (name):
    name = name.replace (" ", "")
    name = name.replace ("?", "")
    name = name.replace (".", "_")
    name = name.replace ("&", "")
    name = name.replace ("(", "")
    name = name.replace (")", "")
    return name

def showProjects(server, isUserLoggedIn):
    request_options = setPagination()
    projects = []

    if isUserLoggedIn == True:
        try:
            all_project_items, pagination_item = server.projects.get(request_options)
            for i in all_project_items: 
                projects.append(i.name)    

        except:
            pass

    return projects


def showWorkbooks(project, server, isUserLoggedIn):
    request_options = setPagination()
    workbooks = []
    
    if isUserLoggedIn == True:
        try:   
            all_workbook_items, pagination_item = server.workbooks.get(request_options)
            for j in all_workbook_items:
                try:
                    if j.project_name == project:
                        workbooks.append(j.name)
                except:
                    pass
        except:
            pass

    return workbooks


def showWorksheets(project, workbook, server, isUserLoggedIn):
    request_options = setPagination()

    worksheets = []
    
    print workbook
    if isUserLoggedIn == True:
        # try:   
        request_options.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                             TSC.RequestOptions.Operator.Equals,
                             workbook))

        matching_workbook_items, pagination_item = server.workbooks.get(request_options)
        for sheet_workbook in matching_workbook_items: 
            if sheet_workbook.project_name == project:
                server.workbooks.populate_views(sheet_workbook)
                for i in sheet_workbook.views:
                    worksheets.append(i.name)
        # except:
        #     pass

    return worksheets


    