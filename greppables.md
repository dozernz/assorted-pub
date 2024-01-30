Regexes for Secrets etc. In grep -E format.

### Loosely valid base64'd JSON

*`{` followed by `['"',"'"," ",'\n','\r']`*

```
(ewo|ew0|eyc|eyL|eyJ|eyI|eyA)
```

### AWS Key ID:

```
(AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{12,}
```

### Azure Principal Secret

* Ref: https://learn.microsoft.com/en-us/purview/sit-defn-azure-ad-client-secret
* Ref: https://github.com/microsoft/azure-pipelines-agent/blob/264f3a14c11a8e039572ae8d54791ea2ea334a54/src/Microsoft.VisualStudio.Services.Agent/AdditionalMaskingRegexes.CredScan.cs#L35

```
[0-9A-Za-z_~\.-]{3}7Q~[0-9A-Za-z_~\.-]{31}|[0-9A-Za-z_~\.-]{3}8Q~[0-9A-Za-z_~\.-]{34}
```

# Other Useful regexes

### UUID4

Not generally fruitful to search for but occasionally useful

```
[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}
```

### Base64

Incredibly false positive prone. Useful for combining with other regexes though.

```
([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)
```

Also possible to search for only base64s of a minimum length (see first capture group, this matches a minimum of 7 times with no max)

```
([A-Za-z0-9+/]{4}){7,}([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)
```
