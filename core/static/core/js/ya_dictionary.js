// Generated by CoffeeScript 1.11.1
(function() {
  this.yaDictFromRus = function(rusWord, langId, successHandler) {
    return $.get({
      url: '/rest/ya_dict/from_rus/',
      data: {
        rus_word: rusWord,
        lang: langId
      },
      success: successHandler
    });
  };

  this.yaDictToRus = function(word, langId, successHandler) {
    return $.get({
      url: '/rest/ya_dict/to_rus/',
      data: {
        word: word,
        lang: langId
      },
      success: successHandler
    });
  };

}).call(this);
