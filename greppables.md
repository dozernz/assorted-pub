Regexes for Secrets etc. In grep -E format.

### Loosely valid base64'd JSON

*`{` followed by `['"',"'"," ",'\n','\r']`*

```
ewo
ew0
eyc
eyL
eyJ
eyI
eyA
```

### AWS Key ID:

```
(AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{12,}
```

### Azure Principal Secret

* Ref: https://learn.microsoft.com/en-us/purview/sit-defn-azure-ad-client-secret
* Ref: https://github.com/microsoft/azure-pipelines-agent/blob/264f3a14c11a8e039572ae8d54791ea2ea334a54/src/Microsoft.VisualStudio.Services.Agent/AdditionalMaskingRegexes.CredScan.cs#L35

```
[0-9A-Za-z_~\.-]{3}7Q~[0-9A-Za-z_~\.-]{31}|[0-9A-Za-z_~\.-]{3}(8|9)Q~[0-9A-Za-z_~\.-]{34}
```

### UUID4

Not generally fruitful to search for but occasionally useful

```
[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}
```
