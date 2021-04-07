from kukres import KUDIGITAL

if __name__ == '__main__':
    try:
        results = KUDIGITAL()
    except Exception as e:
        print('ERROR! ' + str(e))
        quit()
    print('Connected!')
    results.getcatpcha()
    while True:
        print('Available Results:')
        temp = dict()
        for i, event in enumerate(results.events):
            print(f'{i+1}. {event}')
            temp[i+1] = event
        event_id = results.events[temp[int(input('\nSelect: '))]]
        prn = input('Enter PRN: ')
        results.getdata(event_id, prn)
        if results.results:
            print(f'\n{len(results.results)} results found!\n')
            for res in results.results:
                print(f"{res[0]}. {res[2][res[2].find('Sem'):]}")
            res_id = int(input('\nSelect: '))-1
            results.getresult(res_id)
        else:
            print(results.err)
            quit()
        if input('Check Another? (y/[n]): ') != 'y':
            break
