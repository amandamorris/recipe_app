"use strict";

function showHashRecipes(results) {
    for (var hashtag in results) {
        console.log(hashtag)
        for (var recipe of results[hashtag]) {
            console.log(recipe)
            $('#' + hashtag).append("<p>" + recipe[0] + "</p>")
        }
    }

}
$.get('/display_hashed_recipes.json', showHashRecipes);

