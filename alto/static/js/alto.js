window.App = {};
_.extend(App, Backbone.Events);


/* Router */

var Workspace = Backbone.Router.extend({
    routes: {
        'urlpatterns': 'pattern_list',
        'urlpatterns/:pattern_id': 'pattern_detail'
    },
    pattern_list: function() {
        console.log('pattern_list');
    },
    pattern_detail: function (pattern_id) {
        console.log('pattern_detail: ' + pattern_id);
    }
});


/* Models */

var URLPattern = Backbone.Model.extend({
    initialize: function() {},
    getSearchString: function() {
        return this.get('normalized_pattern') + ' ' + this.get('view_module') + '.' + this.get('view_name');
    },
    getTitle: function() {
        return this.get('annotated_pattern');
    },
    getSecondary: function() {
        var modulePath = this.get('view_module');
        var viewName = this.get('view_name');
        return modulePath + '.' + viewName;
    }
});

var URLPatterns = Backbone.Collection.extend({
    model: URLPattern,
    url: 'urlpatterns/'
});

var DjangoView = Backbone.Model.extend({
    initialize: function() {},
    urlRoot: function () {
        return 'views/' + this.get('modulePath') + '/' + this.get('viewName') + '/';
    }
});

var TemplatePath = Backbone.Model.extend({
    initialize: function() {},
    getSearchString: function() {
        return this.get('name');
    },
    getTitle: function() {
        return this.get('name');
    },
    getSecondary: function() {
        return '';
    }
});

var TemplatePaths = Backbone.Collection.extend({
    model: TemplatePath,
    url: 'templates/'
});


/* Views */

var SearchRow = Backbone.View.extend({
    tagName: 'li',
    events: {
        'click': 'select'
    },
    initialize: function() {
    },
    render: function() {
        var ul = $(this.options.parent);
        var main = this.model.getTitle();
        var secondary = this.model.getSecondary();
        $(this.el).html('<a href="#">' + main + '<br>' + secondary +' </a>');
        ul.append(this.el);
        return this;
    },
    select: function(e) {
        e.preventDefault();
        App.trigger('selectedRowChanged', this);
    }
});

var SearchList = Backbone.View.extend({
    initialize: function() {
        this.selectedRow = null;
        this.searchRows = [];
        // Bind the collection's change method to trigger this view's render method.
        // _.bindAll is required so 'this' is correct.
        // Is there a cleaner way to do this?
        _.bindAll(this, 'render');
        this.collection.bind('reset', this.render);

        _.bindAll(this, 'selectedRowChanged');
        App.bind('selectedRowChanged', this.selectedRowChanged);
    },
    render: function() {
        var view = this;
        var ul = this.$el;
        this.$el.html('');
        var results = this.getSearchResults();
        view.searchRows = [];
        _.each(results, function(result) {
            var model = result[1];
            var searchRow = new SearchRow({parent: ul, model: model});
            view.searchRows.push(searchRow);
            searchRow.render();
        });
        return this;
    },
    getSearchResults: function() {
        // Use liquidmetal to score each model against a query string, and
        // return an array of models sorted by descending score.
        var query = $('#search').val();
        var results = [];
        var i = 1.0;
        this.collection.each(function (model) {
            if (query) {
                var candidate = model.getSearchString();
                var score = LiquidMetal.score(candidate, query);
                if (score > 0) {
                    results.push([score, model]);
                }
            } else {
                results.push([-i, model]);
                i = i + 1.0;
            }
        });
        return results.sort(function (a, b) { return b[0] - a[0]; });
    },
    selectedRowChanged: function(row) {
        if (this.selectedRow) {
            this.selectedRow.$el.toggleClass('active');
        }
        row.$el.toggleClass('active');
        this.selectedRow = row;
        App.trigger('selectedModelChanged', row.model);
    },
    selectNextRow: function() {
        if (this.selectedRow) {
            var i = this.searchRows.indexOf(this.selectedRow);
            if (i < this.searchRows.length - 1) {
                App.trigger('selectedRowChanged', this.searchRows[i+1]);
            }
        } else {
            App.trigger('selectedRowChanged', this.searchRows[0]);
        }
    },
    selectPreviousRow: function() {
        if (this.selectedRow) {
            var i = this.searchRows.indexOf(this.selectedRow);
            if (i > 0) {
                App.trigger('selectedRowChanged', this.searchRows[i-1]);
            }
        } else {
            App.trigger('selectedRowChanged', this.searchRows[0]);
        }
    }
});

var ViewPanel = Backbone.View.extend({
    el: '#viewpanel',
    initialize: function() {
        this.model = null;
        var view = this;
        _.bindAll(this, 'selectedModelChanged');
        App.bind('selectedModelChanged', this.selectedModelChanged);
        App.editor = CodeMirror.fromTextArea(document.getElementById('viewcode'), {
            mode: "python",
            theme: "elegant",
            lineWrapping: true,
            lineNumbers: true,
            firstLineNumber: view.line_number,
            readOnly: true
        });
    },
    render: function() {
        var view = this;
        var pattern = this.model.toJSON();
        this.$('#modulename').html(pattern.view_module);
        this.$('#viewname').html(pattern.view_name);
        this.$('#regex').html(pattern.raw_pattern);
        var djangoView = new DjangoView({modulePath: pattern.view_module, viewName: pattern.view_name});
        djangoView.fetch({success: function (model, response) {
            var attributes = model.toJSON();
            view.$('#filename').attr('href', '{{ url_scheme }}://open?url=file://' + attributes.file + '&line=' + attributes.line_number);
            view.$('#filename').text(attributes.file);
            App.editor.setValue(attributes.source);
            App.editor.setOption('firstLineNumber', attributes.line_number);
        }});
    },
    selectedModelChanged: function(model) {
        this.model = model;
        this.render();
    }
});


/* Setup */

$(function () {
    // var root = 'file:///Users/jkocherhans/Projects/urlviz/static/';
    // var workspace = new Workspace();
    // Backbone.history.start({pushState: true, root: root});
    // workspace.navigate('urlpatterns', {trigger: true, replace: false});

    // Initialze with an empty collection. We'll fetch them later.
    // This allows the view to render quickly, but update itself once the
    // real data loads.
    // var collectionName = 'urlpatterns';
    var collectionName = 'templates';
    var collection;
    if (collectionName == 'urlpatterns') {
        collection = new URLPatterns([]);
        var viewPanel = new ViewPanel();
    } else if (collectionName == 'templates') {
        collection = new TemplatePaths([]);
    }
    var searchList = new SearchList({collection: collection, el: $('#searchlist')});
    searchList.render();
    collection.fetch();

    $('#search').focus();
    $('body').bind('keyup', function (e) {
        var activeElement;
        var nextElement;
        if (e.keyCode == 27) {
            $('#search').val('').focus();
            searchList.render();
        } else if (e.keyCode == 38) {
            // Up arrow
            searchList.selectPreviousRow();
        } else if (e.keyCode == 40) {
            // Down arrow
            searchList.selectNextRow();
        }
    });
});
