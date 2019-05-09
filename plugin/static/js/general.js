var graph_padding_delta = 50;
const graph_padding_range = 3;

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

  socket.on("testblah", function(data) {
    console.log(data);
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
