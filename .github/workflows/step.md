```
          README=$(gh api "repos/villgzs/musllinux/contents/README.md" \
                      --jq '.content' | base64 -d)

          echo "Core finished with:"
          echo "${README}"
          echo
          README=$(echo "${README}" | grep "sha:" | head -n 1 )
          echo "${README}"
          README="${README##*: }"
          echo "${README}"

          RUN_JSON=$(gh api "/repos/home-assistant/core/actions/workflows/builder.yml/runs?status=completed&per_page=10" \
            --jq '.workflow_runs[1]')

          printf '%s\n' "$RUN_JSON" | jq .

          RUN_ID=$(echo "$RUN_JSON" | jq -r '.id')
          HEAD_SHA=$(echo "$RUN_JSON" | jq -r '.head_sha')
          # A dev buildnél a verzió tipikusan nightly formátumú (pl. 2026.10.0.dev0)
          # A head_sha rövid formáját és a dátumot használjuk a taghez
          SHORT_SHA=$(echo "$HEAD_SHA" | cut -c1-7)
          # Próbáljuk kiolvasni a display_title-ból vagy a head_branch-ből
          DISPLAY_TITLE=$(echo "$RUN_JSON" | jq -r '.display_title // empty')
          CREATED_AT=$(echo "$RUN_JSON" | jq -r '.created_at' | cut -dT -f1)
          CHECK_SUITE_ID=$(echo "$RUN_JSON" | jq -r '.check_suite_id')
          RUN_CONCLUSION=$(echo "$RUN_JSON" | jq -r '.conclusion')

          echo "Found $RUN_CONCLUSION run on dev:"
          echo "  run_id          = $RUN_ID"
          echo "  check_suite_id  = $CHECK_SUITE_ID"
          echo "  head_sha        = $HEAD_SHA"
          echo "  short_sha       = $SHORT_SHA"
          echo "  created_at      = $CREATED_AT"
          echo "  title           = $DISPLAY_TITLE"
          echo

          # --- Job verzió kinyerése a check suite log ZIP-ből ---
          echo "--- Job verzió kinyerése a check suite log ZIP-ből ---"
          echo
          JOBVERSION=""
          TMPDIR=$(mktemp -d)
          echo "- tempdir: $TMPDIR"
          LOG_ZIP="${TMPDIR}/suite-logs.zip"

          # 1. Letöltés a suites URL-ről (a te példád szerint)
          #    Authentikált letöltés szükséges
          HTTP_CODE=$(curl -sL -o "$LOG_ZIP" -w "%{http_code}" \
            -H "Authorization: Bearer ${GH_TOKEN}" \
            -H "Accept: application/vnd.github+json" \
            "https://github.com/home-assistant/core/suites/${CHECK_SUITE_ID}/logs?attempt=1")

          echo "$HTTP_CODE"

          if [ "$HTTP_CODE" = "200" ] && [ -s "$LOG_ZIP" ]; then
            # 2. Kicsomagolás és a Publish version files log keresése
            unzip -q -o "$LOG_ZIP" -d "$TMPDIR" || true

            # A fájl neve tipikusan: 0_Publish version files.txt (vagy hasonló)
            PUBLISH_LOG=$(find "$TMPDIR" -type f -iname '*Publish*version*files*.txt' | head -1)

            if [ -n "$PUBLISH_LOG" ] && [ -f "$PUBLISH_LOG" ]; then
              # 3. INPUTS_VERSION: 2026.12.0.dev202611030216 kinyerése
              JOBVERSION=$(grep -oE 'INPUTS_VERSION:[[:space:]]*[0-9]+\.[0-9]+\.[0-9]+(\.dev[0-9]+)?' "$PUBLISH_LOG" \
                            | head -1 \
                            | sed -E 's/INPUTS_VERSION:[[:space:]]*//' \
                            || true)
            fi
          else
            echo "::warning::Suite log letöltés sikertelen (HTTP $HTTP_CODE), próbálok API-s fallbacket. 1. próba jelzés"
          fi

          # Fallback 1: teljes run log (API) - sikeres home-Assistant futásoknál ez működött, de a sikertelennél nem adott eredményt
          if [ -z "$JOBVERSION" ]; then
            echo "Fallback 1: Próbálom a /actions/runs/.../logs endpointot..."
            if gh api \
                  -H "Accept: application/vnd.github+json" \
                  "/repos/home-assistant/core/actions/runs/${RUN_ID}/logs" \
                  > "$LOG_ZIP" 2>/dev/null; then
              echo "Fallback 1: Lekérés megtörtént. Kicsomagolás..."
              unzip -q -o "$LOG_ZIP" -d "$TMPDIR" || true
              # ls -las "$TMPDIR"
              PUBLISH_LOG=$(find "$TMPDIR" -type f -iname '*Publish*home-assistant*.txt' | head -1)
              echo "$PUBLISH_LOG"
              if [ -n "$PUBLISH_LOG" ]; then
                JOBVERSION=$(grep -oE 'DOCKER_METADATA_OUTPUT_VERSION:[[:space:]]*[0-9]+\.[0-9]+\.[0-9]+(\.dev[0-9]+)?' "$PUBLISH_LOG" \
                              | head -1 \
                              | sed -E 's/DOCKER_METADATA_OUTPUT_VERSION:[[:space:]]*//' \
                              || true)
              fi
              echo "Fallback 1: lekérés eredménye - JOBVERSION = $JOBVERSION"
            else
              echo "::warning::Fallback 1 API lekérés sikertelen volt."
            fi
          fi


          # Fallback 2: kiadási jegyzék használata a PACKAGES listából
          if [ -z "$JOBVERSION" ]; then
            echo
            echo "Fallback 2: Próbálom a PACKAGES listából kinyerni a tag-eket..."
            JOBVERSION=$(gh api \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            /orgs/home-assistant/packages/container/home-assistant/versions \
            --jq '.[] | select(.metadata.container.tags[]? == "dev") | .metadata.container.tags[]' | head -n 1 )
            echo "- Result of Fallback 2 - JOBVERSON = $JOBVERSION"
          fi

          # Fallback 3: ha még mindig nincs, a régi módszer - de ezt nem akarom...
          if [ -z "$JOBVERSION" ]; then
            echo "::warning::Nem sikerült a jobverziót kinyerni. A nem akarom módszerrel adok TAG-et."
            JOBVERSION="dev-${CREATED_AT}-${SHORT_SHA}"
          fi


          VERSION="$JOBVERSION"

          echo "Found ** ${RUN_CONCLUSION} ** run on dev:"
          echo "  run_id       = $RUN_ID"
          echo "  head_sha     = $HEAD_SHA"
          echo "  short_sha    = $SHORT_SHA"
          echo "  created_at   = $CREATED_AT"
          echo "  title        = $DISPLAY_TITLE"
          echo "  version      = $VERSION"
          echo "  jobversion   = $JOBVERSION"


```
