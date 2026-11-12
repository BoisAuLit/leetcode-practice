class Solution:
    def simplifyPath(self, path):
        dirOrFiles = []
        path = path.split("/")
        for elem in path:
            if dirOrFiles and elem == "..":
                dirOrFiles.pop()
            elif elem not in [".", "", ".."]:
                dirOrFiles.append(elem)

        return "/" + "/".join(dirOrFiles)


s = Solution()
path = "/home/"  # Expecting "/home"
path = "/../"  # Expecting "/"
path = "/home//foo/"  # Expecting "/home/foo"
result = s.simplifyPath(path)
print(result)
