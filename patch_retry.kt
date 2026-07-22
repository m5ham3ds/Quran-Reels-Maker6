        var attempt = 0
        var success = false
        var lastErrorMsg = ""
        while (attempt < 3 && !success) {
            try {
                val response = client.newCall(request).execute()
                if (response.isSuccessful) {
                    // ... the rest of the logic
