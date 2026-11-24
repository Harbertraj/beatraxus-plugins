# BeatRaxus Plugins

Declarative provider catalogue for the [BeatRaxus](https://github.com/Harbertraj/Beatraxus) Android app (schema v1).

> These files are **JSON configuration only**. They never contain DEX, JAR, SO, scripts or bytecode.
> Each `adapterId` points to a reviewed adapter that is already compiled into BeatRaxus.

## Add this repository to BeatRaxus

Open **Add-ons → Add an add-on → Plugin repository** and paste either URL:

```
https://github.com/Harbertraj/beatraxus-plugins
https://raw.githubusercontent.com/Harbertraj/beatraxus-plugins/main/repository.json
```

(If you publish under a different repo name, replace `beatraxus-plugins` with it.)

## Providers

| ID | Category | Adapter | Auth |
|---|---|---|---|
| `jamendo_community` | music_source | `jamendo` | api_key |
| `archive_org_music` | music_source | `archive_org` | none |
| `subsonic_server` | music_source | `subsonic` | server_credentials |
| `archive_org_video` | video_source | `archive_org` | none |
| `jellyfin_server` | video_source | `jellyfin` | server_credentials |
| `emby_server` | video_source | `emby` | server_credentials |
| `stremio_catalog` | video_source | `stremio` | manifest_url |
| `ytxtube_bridge` | video_source | `ytxtube` | none |
| `youtube_audio` | music_source | `youtube_audio` | none |

## Repository layout

```
repository.json        # index (max 512 KiB, max 100 entries)
plugins/<id>.json      # one manifest per provider (max 128 KiB)
scripts/validate.py    # local + CI validation
```

## `repository.json`

```json
{
  "schemaVersion": 1,
  "name": "My BeatRaxus Providers",
  "description": "Short description",
  "plugins": [
    {
      "id": "jamendo_community",
      "name": "Jamendo Music",
      "version": "1.0.0",
      "description": "Free music from independent artists",
      "category": "music_source",
      "adapterId": "jamendo",
      "manifestUrl": "plugins/jamendo_community.json"
    }
  ]
}
```

## `plugins/<id>.json`

```json
{
  "schemaVersion": 1,
  "id": "jamendo_community",
  "name": "Jamendo Music",
  "version": "1.0.0",
  "category": "music_source",
  "adapterId": "jamendo",
  "minAppVersionCode": 8,
  "configuration": { "authType": "api_key" }
}
```

Rules enforced by the app:

- `id` and `adapterId`: letters, digits, underscore, 1–64 chars.
- `version`: `major.minor.patch` with optional `-pre` or `+build` suffix.
- `category`: `music_source`, `metadata`, `lyrics`, `artwork`, `playlist`, `scrobbling`, `video_source`.
- The manifest `id`, `version`, `category` and `adapterId` **must match** the index entry exactly.
- `manifestUrl` is relative to the index URL or an absolute HTTPS URL. No redirects, no credentials in URLs.
- Installable adapters in the current app build: `jamendo`, `archive_org`, `subsonic`, `jellyfin`, `emby`, `stremio`, `ytxtube`. Anything else shows as **Needs app update**.

## Add a new provider

1. Create `plugins/<id>.json`.
2. Add a matching entry to `repository.json`.
3. Run `python3 scripts/validate.py`.
4. Commit and push to `main`.

## Legal

Only list providers that comply with the source service's terms and streaming licences. A repository URL grants no distribution rights.
