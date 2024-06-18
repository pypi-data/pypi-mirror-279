ln = 1 # 0: English; 1: Chinese
LANGS = {
    'en' : 0,
    'zh' : 1,
}


import pytest, os, traceback, sys, threading, shutil, argparse, json, time, zipfile
from .servers import runServers, registClientMsgHandler
from .shared import Testing_State, Settings, LIB_PATH
from .version import VERSION

os.makedirs(Settings.RECORDS_DIR,  exist_ok=True)    
os.makedirs(Settings.RULES_DIR,    exist_ok=True)   

REPORT_TEMPLATE_PATH = os.path.join(LIB_PATH, 'export_report.html')

with open(REPORT_TEMPLATE_PATH,'r',encoding='utf8') as f:
    REPORT_HTML_CONTENT = f.read()

def unloadCaseModules():
 for key in list(sys.modules.keys()):
    lkey = key.lower()
    if lkey.startswith("test_") or \
        lkey.endswith('_test') or \
        'pytest_assist.plugin' == lkey:
        # print('reload ====>',key)
        del sys.modules[key]



class CliMsgHandlers:

    '''
    ******  functions below are runing in websockets thread  **********
    '''


    def get_server_version(msg):
        # print('get_server_version')
        return {
            'event'      : 'result.get_server_version',
            'version'    : VERSION,
        }
       

    def list_history_reports(msg):
        # print('list_history_reports')
        
        if not os.path.exists(Settings.RECORDS_DIR):
            return {
            'event'      : 'result.list_history_reports',
            'items'    : [],
        }
        
        items = sorted([f for f in os.scandir(Settings.RECORDS_DIR) if f.is_dir()], 
                         key=lambda t: t.stat().st_mtime, reverse= True
                         )
        items = [f.name for f in items]

        return {
            'event'    : 'result.list_history_reports',
            'items'    : items,
        }


    def get_history_report(msg):
        filePath = os.path.join(Settings.RECORDS_DIR, msg['name'],'record.json')
        if not os.path.exists(filePath):
            return {
                'event'      : 'result.get_history_report',
                'ret'        : 2,
                'msg'        : 'not exist',
            }
        with open(filePath, 'r', encoding='utf8') as f:
            content = f.read()
       
        return  {
            'event'      : 'result.get_history_report',
            'ret'        : 0,
            'content'    : content,
        }


    def export_this_history_report(msg):
        reportName = msg['name']       

        reportDir = os.path.join(Settings.RECORDS_DIR, reportName)        
        jsonFilePath = os.path.join(reportDir,'record.json')
        if not os.path.exists(jsonFilePath):
            return {
                'event'      : 'result.export_this_history_report',
                'ret'        : 2,
                'msg'        : 'not exist',
            }
        
        
        zipFilePath = os.path.join(Settings.RECORDS_DIR, reportName+'.zip') 
        reportFileLink = f'/{zipFilePath}'.replace('\\','/')

        # already have exported zip file before , just return it
        if os.path.exists(zipFilePath):
            return {
            'event'      : 'result.export_this_history_report',
            'ret'        : 0,
            'link'       : reportFileLink,
        }
         
        
        # create report html
        with open(jsonFilePath, 'r', encoding='utf8') as f:
            report_data_json = f.read()

        reportHtmlFile = os.path.join(reportDir,'report.html')

        with open(reportHtmlFile, 'w', encoding='utf8') as f:
            f.write(REPORT_HTML_CONTENT)
            
            f.write('\n\n<script id="data">\n\nvar report = ')
            f.write(report_data_json)
            f.write('\n\n</script>')
       
        # create zip file
        def zipdir(reportDir, ziph):
            for root, dirs, files in os.walk(reportDir):
                for file in files:
                    if file.endswith('.json') : continue  # my special handle
                    fullPath = os.path.join(root, file)
                    arcName = os.path.relpath(
                        fullPath, 
                        os.path.join(reportDir, '..'))
                    ziph.write(fullPath,arcName)
            
        zf = zipfile.ZipFile(zipFilePath, "w")    
        zipdir(reportDir, zf)
        zf.close()


        return  {
            'event'      : 'result.export_this_history_report',
            'ret'        : 0,
            'link'       : reportFileLink,
        }




    def deleteall_history_reports(msg):
        shutil.rmtree(Settings.RECORDS_DIR, ignore_errors=True)
       
        return {
            'event'      : 'result.deleteall_history_reports',
            'ret'        : 0,
        }

    



    def delete_this_history_report(msg):
        dirPath = os.path.join(Settings.RECORDS_DIR,msg['name'])
        shutil.rmtree(dirPath, ignore_errors=True)

        # also delete exported zip file if exists
        reportZipPath = dirPath+'.zip'
        if os.path.exists(reportZipPath):
            os.remove(reportZipPath)
       
        return  {
            'event'      : 'result.delete_this_history_report',
            'ret'        : 0,
        }




    def list_select_rules(msg):

        if not os.path.exists(Settings.RULES_DIR):
            return {
            'event'      : 'result.list_select_rules',
            'items'    : [],
        }
        
        items = sorted([f for f in os.scandir(Settings.RULES_DIR) if f.is_file()], 
                         key=lambda t: t.stat().st_mtime, reverse= True
                         )
        items = [f.name.replace('.json', '') for f in items]

        return {
            'event'    : 'result.list_select_rules',
            'items'    : items,
        }


    def get_select_rule(msg):
        filePath = os.path.join(Settings.RULES_DIR, msg['name'] + '.json')
        if not os.path.exists(filePath):
            return {
                'event'      : 'result.get_select_rule',
                'ret'        : 2,
                'msg'        : 'not exist',
            }
        with open(filePath, 'r', encoding='utf8') as f:
            content = f.read()
       
        return {
            'event'      : 'result.get_select_rule',
            'ret'        : 0,
            'content'    : content,
        }



    def deleteall_select_rules(msg):
        shutil.rmtree(Settings.RULES_DIR, ignore_errors=True)
       
        return  {
            'event'      : 'result.deleteall_select_rules',
            'ret'        : 0,
        }
  

    def delete_this_select_rule(msg):
        filePath = os.path.join(Settings.RULES_DIR, msg['name']+'.json')
        if os.path.exists(filePath):
            os.remove(filePath)
       
        return {
            'event'      : 'result.delete_this_select_rule',
            'ret'        : 0,
        }



    def save_select_rule(msg):
        name = msg['name']
        if not name:
            name = time.strftime('%Y%m%d-%H%M%S', time.localtime())
            msg['name'] = name

        filePath = os.path.join(Settings.RULES_DIR, name +'.json')
        
        msg.pop('event')

        with open(filePath, 'w', encoding='utf8') as f:
            json.dump(msg, f, ensure_ascii=False, indent=2)
       
        items = sorted([f for f in os.scandir(Settings.RULES_DIR) if f.is_file()], 
                         key=lambda t: t.stat().st_mtime, reverse= True
                         )
        items = [f.name.replace('.json', '') for f in items]

        return {
            'event'      : 'result.save_select_rule',
            'ret'        : 0,
            'items'      : items

        }




    # reft to https://stackoverflow.com/a/62955267
    def collect_cases(msg):
            
        ret  = [[], []]

        class NodeidsCollector:
            def pytest_collection_modifyitems(self, items):
                nodeids = [item.nodeid for item in items]
                ret[0] += nodeids

            def pytest_deselected(self, items):   
                nodeids = [item.nodeid for item in items]
                ret[1] += nodeids

        unloadCaseModules()
        collector = NodeidsCollector()
        pytest.main([
            '--collect-only', 
            '-pno:terminal', 
            ], plugins=[collector])
        
        collected, deselected = ret

        tree = {}

        for one in collected:
            parts = one.split('::')
            
            if parts[0] in tree:
                fo = tree[parts[0]]
            else:
                fo = {'type':'file', 'sub':{}}
                tree[parts[0]] = fo

            fsub = fo['sub']

            # test func
            if len(parts) == 2:
                fsub[parts[1]] = {'type':'func'}

            # test class
            else:            
                if parts[1] in fsub:
                    co = fsub[parts[1]]
                else:
                    co = {'type':'class', 'sub':{}}
                    fsub[parts[1]] = co

                csub = co['sub']
                csub[parts[2]] = {'type':'func'}


        return {
            'event'      : 'result.collect_cases',
            'caseTree'  : tree
        }


    def open_new_test(msg):        

        def runTest(params):        
            try:
                # for multiple runs, the following is to reaload the test modules,
                # in case test files were modified and the modules already loaded
                unloadCaseModules()
               
                args = ['-p pytest_assist.plugin', '--capture=tee-sys'] + params
                print('==>pytest parameters are:',args)
                pytest.main(args)
            except:
                print(traceback.format_exc())


        if Testing_State.inTesting:
            return {
                'event' : 'result.open_new_test',
                'ret'   : 3,
                'info'   : '正在测试中，不能创建新测试'
            }
        
        
        Testing_State.saveRecord = msg['saveRecord']

        testName = msg['name']
        # print('testname000000000000',testName)
        if testName and Testing_State.saveRecord:
            testRecordDir = os.path.join(Settings.RECORDS_DIR,testName)
            if os.path.exists(testRecordDir):
                shutil.rmtree(testRecordDir, ignore_errors=True)
                # ret = {
                #     'event' : 'result.open_new_test',
                #     'ret'   : 1,
                #     'info'   : '同名测试记录已经存在，将被覆盖'
                # }
        
        Testing_State.curTestName = testName

        keys = msg['keys']
        tags = msg['tags']
        nodeIds = msg['nodeIds']

        params = [f'-k {s}' for s in keys] + [f'-m {s}' for s in tags] + nodeIds
        threading.Thread(target=runTest, args=(params,), daemon=True).start()


    def abort_testing(msg):    
        if Testing_State.inTesting:
            Testing_State.quitTesting = True
        else:
            return {
                'event' : 'result.abort_testing',
                'ret'   : 2,
                'info'   : '当前没有测试'
            }


    def force_abort_testing(msg):  
        from subprocess import Popen


        cmd = f'"{sys.executable}" -m pytest_assist --restart ' + ' '.join(sys.argv[1:]) 
        
        # on windows or macos
        if sys.platform == 'win32' or sys.platform == "darwin":        
            Popen(
                args=cmd,
                shell=True
            )     
        # most likely on linux   
        else:      
            # recommend use "nohup python3 -m pytest_assist > /dev/null 2> /dev/null" to start
            cmd = f'nohup {cmd} > /dev/null 2> /dev/null'  
            Popen(
                args=cmd,
                shell=True
            )        

        os._exit(0)


    def kill_pytest_assist(msg):  
        print('\n\n***** pytest assist Exit *******\n\n')        
        exit(0)

methodNames = [attr for attr in dir(CliMsgHandlers) if not attr.startswith('__')]
# print('********* methodNames', methodNames)
for mn in methodNames :
    registClientMsgHandler(mn, getattr(CliMsgHandlers,mn))



# set parameters
def handleArguments() :    
    global ln
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=f'pytest-assist v{VERSION}',
                        help=("显示版本号", 'display pytest-assist version')[ln])
    parser.add_argument('--lang', choices=['en','zh'],
                        help=("设置工具语言", 'set language')[ln])

    parser.add_argument("--host", 
                        default='0.0.0.0',
                        help=['HTTP/WebSocket 服务地址，缺省 0.0.0.0','HTTP/WebSocket host, default is 0.0.0.0'][ln])
    

    parser.add_argument("--port", type=int, default=48530,
                        help=("HTTP 端口，缺省 48530", "HTTP Port, default is 48530")[ln])

    parser.add_argument("--wsport", type=int, default=48531,
                        help=("WebSocket 端口，缺省 48531", "WebSocket Port, default is 48531")[ln])


    parser.add_argument("--restart", action='store_true',
                        help="internal use")
    

    args = parser.parse_args()
    

    # set lang
    if args.lang:
        ln = LANGS[args.lang]

    # host port
    Settings.host = args.host
    Settings.http_port = args.port
    Settings.ws_port = args.wsport

    # to ensure last process exit
    if args.restart:
        import time
        time.sleep(1)

handleArguments()

print(f'''
  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *

  *                   Pytest Assist  v{VERSION}                *

  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
''')

runServers()


    

