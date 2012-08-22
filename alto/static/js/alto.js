(function($) {

var alto = {};
window.alto = alto;
_.extend(alto, Backbone.Events);

alto.initialize = function(options) {
    if (options.mode) {
        alto.mode = options.mode;
    } else {
        alto.mode = 'views';
    }
    alto.url_scheme = options.url_scheme;
    alto.query = options.query;
};

/* Router */

var Workspace = Backbone.Router.extend({
    routes: {
        'views/': 'pattern_list',
        'templates/': 'template_list'
    },
    pattern_list: function() {
        alto.urlPatterns = new URLPatterns([]);
        alto.searchList = new SearchList({collection: alto.urlPatterns, el: $('#searchlist')});
        alto.viewPanel = new ViewPanel();
        alto.searchList.render();
        alto.urlPatterns.fetch();
    },
    template_list: function (pattern_id) {
        alto.tempatePaths = new TemplatePaths([]);
        alto.searchList = new SearchList({collection: alto.tempatePaths, el: $('#searchlist')});
        alto.viewPanel = new CodePanel();
        alto.searchList.render();
        alto.tempatePaths.fetch();
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
    url: '/_alto/template-paths/'
});

var Template = Backbone.Model.extend({
    initialize: function() {},
    urlRoot: function () {
        return '/_alto/templates/' + this.get('name') + '/';
    }
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
        alto.trigger('selectedRowChanged', this);
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
        alto.bind('selectedRowChanged', this.selectedRowChanged);
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
        alto.trigger('selectedModelChanged', row.model);
    },
    selectNextRow: function() {
        if (this.selectedRow) {
            var i = this.searchRows.indexOf(this.selectedRow);
            if (i < this.searchRows.length - 1) {
                alto.trigger('selectedRowChanged', this.searchRows[i+1]);
            }
        } else {
            alto.trigger('selectedRowChanged', this.searchRows[0]);
        }
    },
    selectPreviousRow: function() {
        if (this.selectedRow) {
            var i = this.searchRows.indexOf(this.selectedRow);
            if (i > 0) {
                alto.trigger('selectedRowChanged', this.searchRows[i-1]);
            }
        } else {
            alto.trigger('selectedRowChanged', this.searchRows[0]);
        }
    }
});

var ViewPanel = Backbone.View.extend({
    el: '#panel',
    initialize: function() {
        this.model = null;
        var view = this;
        _.bindAll(this, 'selectedModelChanged');
        alto.bind('selectedModelChanged', this.selectedModelChanged);
        alto.editor = CodeMirror.fromTextArea(document.getElementById('viewcode'), {
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
        this.$('#paneldetails').html('');
        this.$('h2').html(pattern.view_name);
        this.$('#paneldetails').append('<p id="modulename">' + pattern.view_module + '</p>');
        this.$('#paneldetails').append('<code id="regex">' + pattern.raw_pattern + '</code>');
        var djangoView = new DjangoView({modulePath: pattern.view_module, viewName: pattern.view_name});
        djangoView.fetch({success: function (model, response) {
            var attributes = model.toJSON();
            var url = alto.url_scheme + '://open?url=file://' + attributes.file + '&line=' + attributes.line_number;
            $('#filename').html('<a href="' + url + '">' + attributes.file + '</a>');
            alto.editor.setValue(attributes.source);
            alto.editor.setOption('firstLineNumber', attributes.line_number);
        }});
    },
    selectedModelChanged: function(model) {
        this.model = model;
        this.render();
    }
});


var CodePanel = Backbone.View.extend({
    el: '#panel',
    initialize: function() {
        this.model = null;
        var view = this;
        _.bindAll(this, 'selectedModelChanged');
        alto.bind('selectedModelChanged', this.selectedModelChanged);
        alto.editor = CodeMirror.fromTextArea(document.getElementById('viewcode'), {
            mode: "htmlmixed",
            theme: "elegant",
            lineWrapping: true,
            lineNumbers: true,
            readOnly: true
        });
    },
    render: function() {
        var view = this;
        this.$('h2').html(this.model.get('name'));
        view.$('#paneldetails').html('');
        var template = new Template({name: this.model.get('name')});
        template.fetch({success: function (model, response) {
            var attributes = model.toJSON();
            var url = alto.url_scheme + '://open?url=file://' + attributes.file;
            $('#filename').html('<a href="' + url + '">' + attributes.file + '</a>');
            alto.editor.setValue(attributes.source);
            _.each(attributes.parents, function(parent) {
                var url = alto.url_scheme + '://open?url=file://' + parent.file;
                view.$('#paneldetails').append('<li><a href="' + url + '">' + parent.name + '</a></li>');
            });
        }});
    },
    selectedModelChanged: function(model) {
        this.model = model;
        this.render();
    }
});


/* Setup */

$(function () {
    var root = '/_alto/';
    var workspace = new Workspace();
    Backbone.history.start({pushState: true, root: root});
    workspace.navigate(alto.mode + '/', {trigger: true});

    $('#search').focus();
    $('body').bind('keyup', function (e) {
        var activeElement;
        var nextElement;
        if (e.keyCode == 27) {
            // Esc
            $('#search').val('').focus();
            alto.searchList.render();
        } else if (e.keyCode == 38) {
            // Up arrow
            alto.searchList.selectPreviousRow();
        } else if (e.keyCode == 40) {
            // Down arrow
            alto.searchList.selectNextRow();
        } else {
            alto.searchList.render();
        }
    });
});

})(jQuery);
