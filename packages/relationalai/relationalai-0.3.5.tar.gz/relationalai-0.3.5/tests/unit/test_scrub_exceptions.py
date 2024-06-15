from relationalai.clients.util import scrub_exception

# contents: `{"relation_count": 1}` in an internal account
url = "https://sfc-prod3-ds1-27-customer-stage.s3.us-west-2.amazonaws.com/z00j0000-s/stages/c0e19bda-0e9b-47b2-a21d-cfcdd5a16945/transaction-results/01b458ec-0002-6d1e-0051-c00704e7a71a/relation-count.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAXYKJQIRCBD5PYLZS%2F20240515%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240515T154106Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEAaCXVzLXdlc3QtMiJGMEQCIC8EHn51SngV94nYpQBrKBPZ%2B%2Fiifzpj3u15FAMFyM5rAiBSsNFEILg7%2FpucuFhcYMsjAGIpZADIzlpemCEsNZBBjCrJAwip%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDUzMzI2Njk3Mzc2NCIMxWhZCLdXnNlNL8YMKp0Do8jSddBWhvb4Z4IBXWcJ7vjuGbai418ToGUAAS9%2B5Kq7j0%2BP7Lbsh0mZ87VtDf0FXjkYyW4fD1flAB%2Fi0MFeGfPOkAoC7l0aBx1aOAE39iAGL5EgNDvKubUt7i3cWPe7wiubDrZMKhV6yoeVMjHZu2rOsoYl%2F2A2gfK%2By8K2Kvojlbfsx3%2Bie%2FuHNSVC%2FrUif%2BZuPcNJjtXxjpHb2LxZcyxnVYCDChdCtFG4%2BPsG55woeGJXgUQGSF3g8fdEZ7XckTpbn%2FE9leGOEqourELgjJdPpwXzjXZYs2y%2FFtxFuSOofghi9B9Lh9gfcKuWTfKhiambpz9hm1oN8caeUVnZG1o0c8VZ0ZecBY84elMv%2F5PElno4unDTnSmCqDB7aMdMlS6i9sO0J5NKnJ4HUjR%2BHT7UuOAljBlT1b2jSvPQncOkhtLila7hYeq1X1YVZNg7SkwI3ZZz5y5Xu0kWjLKR9tElN5%2B%2BoukHxtLYH7wU6FRMGtcyW%2BtPAH33VxQX6BQ7Fy4%2B6veydANT%2FaAp8XiB5dvEp6Kz5pEDOkm61u8w5a6TsgY6mgHMzNSd8ffllHz6PUsXLlgalp%2FXWnu%2B9aUy1dGMT46jFEfhJrwq5p48R7PE9qKYx0rjPuO5z5hkI2OZlu2iFTJ02biWuR2AzGC3becjqBsA0l2Dcsdp5U5U0GmSPAgL4mByhGsKvVB5i6Qj08irY5%2FPzAdZz4Nhy68sm8W81bgLNdpk7vGEx5Q8eNGX3P3DiGgHd82dVK9hrfa1&X-Amz-SignedHeaders=host&X-Amz-Signature=6145b734ae683536221b4d5d5cc379df3cc7211e4bd72381b88fcbb2eaf78dc4"

def test_scrub_exceptions():
    # exception with scrubbed URL
    exc = Exception(f"connection refused to {url}")
    scrubbed_exc = scrub_exception(exc)
    assert scrubbed_exc.message == "connection refused to https://sfc-prod3-ds1-27-customer-stage.s3.us-west-2.amazonaws.com/z00j0000-s/stages/c0e19bda-0e9b-47b2-a21d-cfcdd5a16945/transaction-results/01b458ec-0002-6d1e-0051-c00704e7a71a/relation-count.json?X-Amz-Algorithm=XXX&X-Amz-Credential=XXX&X-Amz-Date=XXX&X-Amz-Expires=XXX&X-Amz-Security-Token=XXX&X-Amz-SignedHeaders=XXX&X-Amz-Signature=XXX"
    
    exc2 = Exception("some other error")
    scrubbed_exc2 = scrub_exception(exc2)
    assert scrubbed_exc2 == exc2
