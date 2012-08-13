window.App = {};
_.extend(App, Backbone.Events);
App.selectedPattern = null;


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
    initialize: function() {}
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

/* Views */

var URLPatternRow = Backbone.View.extend({
    tagName: 'li',
    className: 'urlpattern',
    events: {
        'click': 'selectPattern'
    },
    render: function() {
        var ul = $(this.options.parent);
        var pattern = this.model.toJSON();
        var regex = pattern.annotated_pattern;
        $(this.el).html('<a href="#">' + regex + '<br>' + pattern.view_module + '.' + pattern.view_name +' </a>');
        ul.append(this.el);
        return this;
    },
    selectPattern: function(e) {
        e.preventDefault();
        $(this.el).toggleClass('active');
        App.selectedPattern = this.model;
        App.trigger('selectedPatternChanged', 'testing');
    }
});

var URLPatternListView = Backbone.View.extend({
    events: {
        'click li': 'selectPattern'
    },
    initialize: function() {
        var view = this;
        this.activeView = null;
        this._patternViews = [];
        _.bindAll(this, 'render');
        this.collection.bind('reset', this.render);
    },
    render: function() {
        var view = this;
        var ul = this.$el;
        this.$el.html('');

        // Sort/filter the collection if needed
        var results = [];
        var query = $('#search').val();

        var i = 1.0;
        this.collection.each(function (pattern) {
            if (query) {
                var candidate = pattern.get('normalized_pattern') + ' ' + pattern.get('view_module') + '.' + pattern.get('view_name');
                var score = LiquidMetal.score(candidate, query);
                if (score > 0) {
                    results.push([score, pattern]);
                }
            } else {
                results.push([-i, pattern]);
                i = i + 1.0;
            }
        });

        results = results.sort(function (a, b) { return b[0] - a[0]; });

        _.each(results, function(result) {
            var pattern = result[1];
            var subView = new URLPatternRow({parent: ul, model: pattern});
            view._patternViews.push(subView);
            subView.render();
        });
        return this;
    },
    selectPattern: function(e) {
        $(this.activeElement).removeClass('active');
        this.activeElement = e.currentTarget;
    }
});

var ViewPanel = Backbone.View.extend({
    el: '#viewpanel',
    initialize: function() {
        var view = this;
        _.bindAll(this, 'render');
        App.bind('selectedPatternChanged', this.render);
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
        var pattern = App.selectedPattern.toJSON();
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
    }
});

/* Setup */

$(function () {
    var root = 'file:///Users/jkocherhans/Projects/urlviz/static/';
    var workspace = new Workspace();
    Backbone.history.start({pushState: true, root: root});
    //workspace.navigate('urlpatterns', {trigger: true, replace: false});

    var urlPatterns = new URLPatterns([]);

    var urlPatternListView = new URLPatternListView({
        collection: urlPatterns,
        el: $('#urlpatterns')
    });
    urlPatternListView.render();

    var viewPanel = new ViewPanel();

    urlPatterns.fetch();

    $('#search').focus();
    $('#searchform').bind('keyup', function (e) {
        if (e.keyCode == 38 || e.keyCode == 40) {
        } else {
            urlPatternListView.render();
            $('#urlpatterns').children('li.urlpattern').first().click();
        }
    });
    $('body').bind('keyup', function (e) {
        var activeElement;
        var nextElement;
        if (e.keyCode == 27) {
            $('#search').val('').focus();
            urlPatternListView.render();
        } else if (e.keyCode == 38) {
            // Up arrow
            if (App.selectedPattern !== null) {
                activeElement = $('li.active');
                nextElement = activeElement.prev('li.urlpattern');
                nextElement.click();
            } else {
                $('#urlpatterns').children('li.urlpattern').first().click();
            }
        } else if (e.keyCode == 40) {
            // Down arrow
            if (App.selectedPattern !== null) {
                activeElement = $('li.active');
                nextElement = activeElement.next('li.urlpattern');
                nextElement.click();
            } else {
                $('#urlpatterns').children('li.urlpattern').first().click();
            }
        }
    });
});
