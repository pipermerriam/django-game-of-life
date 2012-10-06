// The lowest level component, a single cell on the game board.
var Cell = Backbone.Model.extend({
  urlRoot: '/cells/',
  initialize: function() {
    if(!this.get('id')) {
      this.set('url', '/world/' + (String)(this.get('world')) + '/cells/' + (String)(this.get('x')) + '/' + (String)(this.get('y')) + '/');
    }
  }
});

// The view for each cell.
var CellView = Backbone.View.extend({
  tagName: "div",
  className: "cell",
  event: {
    "click": "openDialog",
  },

  attributes: function() {
    attrs = {};
    classes = ['cell',];
    if(!(this.model.get('id') === undefined)) {
      attrs['id'] == 'cell_' + (String)(this.model.get('id'));
    }
    if(this.model.get('is_alive') === true) {
      classes.concat(['is_alive',]);
    }
    attrs['class'] = classes.join(' ');
    return attrs;
  },

  render: function() {
    // Replace with better render function.
    $(this.el).html('<div></div>');
    return this;
  },

  openDialog: function() {
    // Replace with dialog box for modifying cell
  },
});

/*
 *  Stores basic world information.
 */
var World = Backbone.Model.extend({
  defaults: {
      x_size: 20,
      y_size: 15,
      x: 0,
      y: 0,
  },
  urlRoot: '/world/',
});

/*
 *  Game Board
 */
var Board = Backbone.Collection.extend({
  model: Cell,
  initialize: function() {
    this.cells = [];
    _.each(this.models, function(cell) {
      this.setCell(cell.get('x'), cell.get('y'), cell);
    });
  },

  url: function() {
    return this.world.url() + '/cells/';
  },
  /*
   * getCell(x, y)
   *
   * Gets a cell from the internal cell buffer.  If no cell is found, a new
   * cell is initialized.
   */
  getCell: function(x, y) {
    if(this.cells[y] === undefined) {
      this.cells[y] = [];
    }
    if(this.cells[y][x] === undefined) {
      cell = new Cell({
        x: x,
        y: y,
      });
      cell.fetch();
    } else {
      cell = this.cells[y][x];
    }
    return cell;
  },
  /*
   * setCell(x, y, cell)
   *
   * Sets a cell to the internal cell buffer.
   */
  setCell: function(x, y, cell) {
    if(this.cells[y] === undefined) {
      this.cells[y] = [];
    }
    this.cells[y][x] = cell;
  },
});

var BoardView = Backbone.Collection.extend({
  tagName: "div",
  className: "board",
  render: function() {
    // render the game board
  }
});

//
// Ajax Send CSRF Protection
// https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
//
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
