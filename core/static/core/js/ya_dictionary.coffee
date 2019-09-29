@yaDictFromRus = (rusWord, langId, successHandler) ->
    $.get({
        url: '/rest/ya_dict/from_rus/'
        data:
            rus_word: rusWord
            lang: langId
        success: successHandler
    })

@yaDictToRus = (word, langId, successHandler) ->
    $.get({
        url: '/rest/ya_dict/to_rus/'
        data:
            word: word
            lang: langId
        success: successHandler
    })
