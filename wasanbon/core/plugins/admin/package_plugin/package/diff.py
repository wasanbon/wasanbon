
class PackageDiff():
    def __init__(self, repo1, repo2):
        self.repos = (repo1, repo2)
        pass

    @property
    def rtcs(self):
        rtcs1 = self.repos[0].rtcs
        rtcs2 = self.repos[1].rtcs
        plus_rtcs = []
        minus_rtcs = []
        for rtc1 in rtcs1:
            match_flag = False
            for rtc2 in rtcs2:
                if rtc1.name == rtc2.name:
                    match_flag = True
            if not match_flag:
                plus_rtcs.append(rtc1)


        for rtc2 in rtcs2:
            match_flag = False
            for rtc1 in rtcs1:
                if rtc2.name == rtc1.name:
                    match_flag = True
            if not match_flag:
                minus_rtcs.append(rtc2)

        return [plus_rtcs, minus_rtcs]
