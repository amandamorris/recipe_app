"use strict";
// TODO: look into import/export statements for javascript

var is_user_page = (window.location.pathname.indexOf("users") > -1);
var is_search_results_page = (window.location.pathname.indexOf("recipe_search") > -1);

// If on a recipe search, ajax call to view each recipe
if (is_search_results_page) {
    $('.recipe-container').each(function() {
        var recipe_id = $( this ).data("id");
        var formInput = {
            "recipe_id": recipe_id
        };
    // console.log(formInput);
        $.post("/view_recipe.json", formInput, getRecipe);
        });
}

function displayRecipe(result, container_id, hashtag_name) {
    // Adds html with recipe details to the html element with container_id
    // Called by fetchRecipe

    // console.log("insertDiv", result,container_id, hashtag_name);
    var container = $("#"+container_id);

    var recipe_name = result.recipe_name;

    var recipe_id = result.recipe_id.toString();

    var div_id;
    // If on user page, div id is dependent on hashtag/starring
    if (is_user_page) {
        if (!hashtag_name) {
            div_id = "starring-" + recipe_id;
        } else {
            div_id = hashtag_name + "-" + recipe_id;
        }
    } else {
        div_id = "recipe-" + recipe_id;
    }
    var recipeDetails = `
        <div class=recipe_details id=${div_id}>
            <h4><a href=#details-${div_id} data-toggle="collapse">${recipe_name}
            </a></h4>
            <span>Total time:${result.total_time} minutes</span>
            <div class=row>
                <div class="col-xs-3">
                    <img src=${result.images} style=width:150px;height:150px;>
                </div>
        `;
    var searchHashtagInfo = `<div>Current hashtags: <span id=hashtags-${result.recipe_id}>`;
    var ingredients = "";
    for (var ingredient of result.ingredients) {
        var newIngred;
        if (ingredient.unit !== null) {
            newIngred = `<p>${ingredient.quantity} ${ingredient.unit} ${ingredient.ingredient_name}</p>`;
            } else {
                newIngred =`<p>${ingredient.quantity} ${ingredient.ingredient_name}</p>`;
            }
        ingredients += newIngred;
        }
    var steps = `<b>Instructions</b> <div>${result.steps}</div>`;
    if ((is_search_results_page) && (result.username)) {

        recipeDetails += `<div class="col-xs-9">`;
        recipeDetails += result.starButton;

        var recipe_hashtags = result.tags;
        for (var hashtag of recipe_hashtags) {
            searchHashtagInfo += `${hashtag} `;
        }
        searchHashtagInfo += `</span></div>`;
        recipeDetails += searchHashtagInfo;
        
        recipeDetails += result['dropdownMenus'];
        recipeDetails += `</div></div>`;

    } else {
        recipeDetails += `<div class="col-xs-9"></div></div>`;
    }
    recipeDetails += `
            <div id=details-${div_id} class=collapse>
                <div><b>Ingredients</b></div><div>${ingredients}</div>
                <div>${steps}</div>
            </div>
        </div>
        `;
    container.append(recipeDetails);

    if (result.is_starring === "false") {
        $(`#star-button-${result.recipe_id}`).html(`
            <span class="glyphicon glyphicon-star" aria-hidden="true"></span>
            Star Recipe
            <span class="glyphicon glyphicon-star" aria-hidden="true"></span>`);
    }

    if (result.is_starring === "true") {
        $(`#star-button-${result.recipe_id}`).html("Recipe starred");
    }
}

function fetchRecipe(recipe_id, container_id, hashtag) {
    // Given a recipe_id and container_id, get the recipe details from the
    // server, and call displayRecipe, passing in the recipe details and
    // container_id
    // Called by gethashrecipes

    //  TODO: check if I need this
    var formInput = {
                "recipe_id": recipe_id,
                "container_id": container_id
                };
    // console.log(formInput);
    $.post("/view_recipe.json", formInput, function(results) {
            displayRecipe(results, container_id, hashtag);
            });
}
function getHashRecipes(results) {
    // For each of a user's hashtag, create a div (container) for that hashtag,
    // and for each recipe tagged with the hashtag, call fetchRecipe, sending
    // the recipe_id and container_id
    // Callback function for '/display_hashed_recipes.json' get request
    var hashContainer = $("#hashtag-container");
    for (var hashtag in results) {
        hashContainer.append(`
            <div id=${results[hashtag].hashtag_id}>
            <h2>${hashtag}</h2>
            </div>`);
        }
    for (var hashtag in results) {
        var container_id = results[hashtag]["hashtag_id"];
        for (var recipe of results[hashtag]["recipes"]) {
            fetchRecipe(recipe[0],container_id, hashtag);
        }
    }
}

function getStarredRecipes(results) {
    // For each recipe a user starred, call fetchRecipe, sending
    // the recipe_id and container_id for starrings
    // Callback function for '/display_starred_recipes.json' get request
    var container_id = "starring-container";
    // console.log(container_id);
    var starrings = results["recipes"];
    // console.log(starrings);
    for (var recipe_id of starrings) {
        // console.log(recipe_id);
        fetchRecipe(recipe_id, container_id);
    }
}
// If on a user's page, ajax call to get starred and hashed recipes
if (is_user_page) {
    $.get('/display_starred_recipes.json', getStarredRecipes);
    // Get list of user's hashtag (and for each, also hashtagged recipes)
    $.get('/display_hashed_recipes.json', getHashRecipes);
    }

function getRecipe(results) {
    // console.log(results);
    var recipe_id = results.recipe_id;
    var recipe_id = results.recipe_id;
    var container_id = `div-${recipe_id}`;
    // TODO: THINK ABOUT RENAMING RESULTS[TAGS] TO SOMETHING ELSE
    var recipe_hashtags = results['tags'];
    // console.log(results, container_id);
    // If user is logged in, create string html of dropdown hashtag menus
    // console.log(results);
    if (results.username) {
        results['dropdownMenus'] = createDropdowns(results.user_hashtags,
                                                   recipe_id,
                                                   recipe_hashtags
                                                   );
        var starButton = `
            <button type="button"
                class="star-btn btn btn-success"
                id=star-button-${recipe_id}
                data-id=${recipe_id}></button>
            `;
        results['starButton'] = starButton;
        }
    displayRecipe(results, container_id);
}

function createDropdowns(user_hashtags, recipe_id, recipe_hashtags) {
    // Create dropdown menus to add and delete a hashtag
    // Called by getRecipe
    var addHashDropdown = `
        <div class="dropdown">
        <button class="btn btn-warning dropdown-toggle" id="menu1"
            type="button" data-toggle="dropdown">
        Add a hashtag <span class="caret"></span></button>
        <ul class="dropdown-menu" role="menu" aria-labelledby="menu1">
        `
    // var userHashtagList = `<datalist id="userhashtaglist">`;
    for (var hashtag of user_hashtags) {
        addHashDropdown += `
            <li role="presentation">
            <a class="add-hashtag" role="menuitem" id=dropdown-${hashtag}
            tabindex="-1" href="#" data-recipe_id=${recipe_id}
            data-hashtag=${hashtag}>${hashtag}
            </a></li>
            `;
            // userHashtagList += `<option value=${hashtag}>`
        }
    addHashDropdown += `
        <input type="text" id="new-hashtag" data-recipe_id=${recipe_id}
        placeholder="Create a hashtag"/></a>
        </ul></div>
        <div id="new_hashtag"></div>
        `;

    var delHashDropdown = `
            <div class="dropdown">
            <button class="btn btn-danger dropdown-toggle" id=$(#del-hashtag-${recipe_id})
                type="button" data-toggle="dropdown">
            Remove a hashtag <span class="caret"></span></button>
            <ul class="dropdown-menu" role="menu" aria-labelledby=$(#del-hashtag-${recipe_id})>
            `;
    for (var hashtag of recipe_hashtags) {
        delHashDropdown += `
            <li role="presentation">
            <a class="del-hashtag" role="menuitem" id=del-dropdown-${hashtag}
            tabindex="-1" href="#" data-recipe_id=${recipe_id}
            data-hashtag=${hashtag}>${hashtag}
            </a></li>
            `;
        // console.log(hashtag[0]);
    }
    delHashDropdown += `</div>`;

    var bothDropdowns = addHashDropdown.concat(delHashDropdown);
    return bothDropdowns;

}

// Add event listener for selecting a hashtag from dropdown menu
$('.recipe-container').on('click', "a.add-hashtag", function(evt) {
    var hashtagName = $( this ).data("hashtag");
    var recipeId = $( this ).data("recipe_id");
    var formInput = {
        "recipe_id": recipeId,
        "hashtag_name": hashtagName
    };
    // console.log(formInput);
    $.post("/add_hashtag.json", formInput, populateHash);
    // addHashtag(hashtagName, recipeId);
});

// Add event listener for creating a new hashtag in text box
$('.recipe-container').on('keypress', "#new-hashtag", function(evt) {
    var key = evt.which;
    if(key == 13)  // the enter key
        {
            var hashtagName = $(this).val();
            var recipeId = $( this ).data("recipe_id");
            var formInput = {
                "recipe_id": recipeId,
                "hashtag_name": hashtagName
            };
            // console.log(formInput);
            $.post("/add_hashtag.json", formInput, populateHash);
            // addHashtag(hashtagName, recipeId);
        }
}); 

// Add event listener for deleting hashtag from dropdown menu
$('.recipe-container').on('click', "a.del-hashtag", function(evt) {
    var hashtagName = $( this ).data("hashtag");
    var recipeId = $( this ).data("recipe_id");

    var formInput = {
        "recipe_id": recipeId,
        "hashtag_name": hashtagName
    };
    $.post("/del_hashtagization.json", formInput, updateDeletedHash);
    // delHashtagization(hashtagName, recipeId);
});

// $('.recipe-container').on('click', $('.star-btn'), starRecipe);
$('.recipe-container').on('click', '.star-btn', function(evt) {
    var recipe_id = $( this ).data('id');

    // console.log(recipe_id);
    var formInput = {
        "recipe_id": recipe_id
    };
    $( this ).html("Recipe starred");
    $.post("/star_recipe.json", formInput, console.log("recipe starred"));

});

function populateHash(results) {
    var recipe_id = results["recipe_id"];
    var hashtag = results['hashtag_name'];
    if (typeof $('#hashtags-' + recipe_id).innerHTML != 'undefined') {
            $('#hashtags-' + recipe_id).innerHTML = $('#hashtags-' + recipe_id).innerHTML + results['hashtag_name'] + " ";
    } else {
        $('#hashtags-' + recipe_id).innerHTML = `Current hashtags: ${hashtag} `;
    }

    $('#del-hashtag-' + recipe_id).append("<option value=" + results['hashtag_name'] + ">" + results['hashtag_name'] + "</option>")
}

function updateDeletedHash(results) {
    var recipe_id = results["recipe_id"];
    var hashtags = results["hashtags"];
    var del_tag = results["del_tag"];
    // console.log(recipe_id, hashtags);
    // empty the div populated with the recipe's hashtags
    $('#hashtags-' + recipe_id).empty();
    // repopulate the div with the updated list of hashtags
    for (var hashtag of hashtags) {
        $('#hashtags-' + recipe_id).append(hashtag);
        $('#hashtags-' + recipe_id).append(" ");
    }
}

