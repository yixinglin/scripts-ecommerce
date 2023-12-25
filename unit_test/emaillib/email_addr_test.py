from pylib.httputils import check_email_address

# C:\Users\Lin\Desktop\newsletter
# check_email_address

if __name__ == '__main__':
    file = r"C:\Users\Lin\Desktop\newsletter\list_customer.csv"
    emails = []
    with open(file, 'r') as fp:
        # emails = [li.strip() for li in fp.readlines()]
        emails = list(map(lambda o: o.strip(), fp.readlines()))
        emails = emails[1:]


    for e in emails:
        is_ = check_email_address(e)
        print(is_, e)
        assert is_ == True
    # aa = ["Steva69@Web.de"]
    print(check_email_address("a.sack@S1-Event.de"))