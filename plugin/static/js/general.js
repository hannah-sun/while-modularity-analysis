var graph_padding_delta = 50;
const graph_padding_range = 3;

var COLORS = [
  "#ef5350",
  "#ab47bc",
  "#5c6bc0",
  "#29b6f6",
  "#9ccc65",
  "#ffca28",
  "#ff7043",
];

$(function() {
  /* where 150 is the max-width of the .analysis-graph-edge and
   * 50 is the minimum padding to the side of the tab window */
  graph_padding_delta = Math.min(
      $("#plugin-graph-tab").width() / 2 - 150 - 50, graph_padding_delta);

  function toggle_write() {
    $("#plugin-tab-content-graph").toggleClass("hide-left-edges",
        !$("#plugin-toggle-write-edges").prop("checked"))
  }
  toggle_write();
  $("#plugin-toggle-write-edges").on("input", toggle_write);

  function toggle_read() {
    $("#plugin-tab-content-graph").toggleClass("hide-right-edges",
        !$("#plugin-toggle-read-edges").prop("checked"))
  }
  toggle_read();
  $("#plugin-toggle-read-edges").on("input", toggle_read);
});

function while_plugin(socket) {

  socket.on("plugin_analysissnippets", function(data) {
    const $tab = $("#plugin-snippets-tab");

    $tab
      .removeClass("loading")
      .toggleClass("error", data.error);

    $tab.find(".tab-body").removeClass("staging");

    if (!data.error) {
      const $content = $tab.find("#plugin-tab-content-snippets");
      $content.empty();

      var node_elems = [];

      var nodes = data.snippet_data.nodes;
      for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        if (node === null) {
          node_elems.push(null);
          continue;
        }

        node = node
          .replace(/\n /g, "<br>    ")
          .replace(/\n/g, "<br>")
          .replace(/ /g, "&nbsp;");

        var $elem = $(
          '<div class="snippet-container">' +
            '<div class="snippet-node" nodeid="' + i + '">' +
              node +
            '</div>' +
          '</div>'
        );
        $content.append($elem);
        node_elems.push({
          container: $elem,
          node: $elem.find(".snippet-node"),
        });
      }

      var snippets = data.snippet_data.snippets;
      var color_idx = 0;
      for (var i = 0; i < snippets.length; i++) {
        var snippet = snippets[i];
        var color = COLORS[color_idx % COLORS.length];
        color_idx += 1;
        snippet.sort(function(a, b) {
          return parseInt(a) - parseInt(b);
        })
        for (var j = 0; j < snippet.length; j++) {
          var node_obj = node_elems[snippet[j]];
          node_obj.node.css("background", color);

          if (j < snippet.length - 1) {
            var next_idx = snippet[j + 1];

            var contiguous = true;
            for (var k = snippet[j] + 1; k < next_idx; k++) {
              if (node_elems[k] !== null) {
                contiguous = false;
                break;
              }
            }

            if (contiguous) {
              node_obj.container.addClass("merge-next");
            }
          }
        }
      }
    }
  });

  socket.on("plugin_analysisgraph", function(data) {
    const $tab = $("#plugin-graph-tab");

    $tab
      .removeClass("loading")
      .toggleClass("error", data.error);

    $tab.find(".tab-body").removeClass("staging");

    if (!data.error) {
      const $content = $tab.find("#plugin-tab-content-graph");
      $content.empty();

      var nodes = [];

      const edge_settings = {
        left: {
          cls: "analysis-graph-edge left-edge",
          padding_css: "paddingRight",
          cnt: 0,
        },
        right: {
          cls: "analysis-graph-edge right-edge",
          padding_css: "paddingLeft",
          cnt: 0,
        },
      };
      function draw_edge(i, j, side) {
        const node1 = nodes[i];
        const node2 = nodes[j];

        const mid1 = node1.position().top + node1.outerHeight(true) / 2.0;
        const mid2 = node2.position().top + node2.outerHeight(true) / 2.0;

        var $edge = $(
          '<div class="' + edge_settings[side].cls + '"></div>'
        );

        $edge.addClass("edge-connected-" + i).addClass("edge-connected-" + j);


        const padding = ((edge_settings[side].cnt % graph_padding_range + 1) *
            (graph_padding_delta / graph_padding_range));

        /* in height: -2 is the border width of the edge */
        $edge
          .css("height", Math.max(mid1, mid2) - Math.min(mid1, mid2) - 2)
          .css("top", Math.min(mid1, mid2))
          .css(edge_settings[side].padding_css, padding);

        $content.append($edge);
        edge_settings[side].cnt += 1;
      }

      var graph = data.graph;
      for (var i = 0; i < graph.length; i++) {
        var node = graph[i];
        var $elem = $(
          '<div class="analysis-graph-node-container">' +
            '<div class="analysis-graph-node" nodeid="' + i + '">' +
              node.label +
            '</div>' +
          '</div>'
        );
        $content.append($elem);
        nodes.push($elem);

        if (node.write_edges.length > 0) {
          for (var j = 0; j < node.write_edges.length; j++) {
            draw_edge(node.write_edges[j], i, "left");
          }
        }

        if (node.read_edges.length > 0) {
          for (var j = 0; j < node.read_edges.length; j++) {
            draw_edge(node.read_edges[j], i, "right");
          }
        }

        $elem.find(".analysis-graph-node")
          .mouseenter(function() {
            $content.find(".analysis-graph-edge")
                .toggleClass("inactive", true);
            $content.find(".edge-connected-" + this.getAttribute("nodeid"))
                .toggleClass("inactive", false);
          })
          .mouseleave(function() {
            $content
                .find(".analysis-graph-edge").toggleClass("inactive", false);
          });
      }
    }

  });
}
