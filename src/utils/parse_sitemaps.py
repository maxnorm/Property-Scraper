

def parse_daily_sitemap(result):
    result["url"] = result[result["url"].str.contains("/fr/")]["url"]
    result.dropna(inplace=True)
    result["url"] = result[result["url"].str.contains("a-vendre")]["url"]
    result.dropna(inplace=True)
    return result


def parse_global_sitemap(result):
    result["url"] = result[result["url"].str.contains("properties")]["url"]
    result.dropna(inplace=True)
    return result

