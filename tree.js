
///////// Spinner 

var opts = {
  lines: 13, // The number of lines to draw
  length: 7, // The length of each line
  width: 4, // The line thickness
  radius: 10, // The radius of the inner circle
  rotate: 0, // The rotation offset
  color: 'steelblue', // #rgb or #rrggbb
  speed: 1, // Rounds per second
  trail: 60, // Afterglow percentage
  shadow: false, // Whether to render a shadow
  hwaccel: false, // Whether to use hardware acceleration
  className: 'spinner', // The CSS class to assign to the spinner
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  top: 'auto', // Top position relative to parent in px
  left: 'auto' // Left position relative to parent in px
};
var spinner = new Spinner(opts).spin();
$("#loading").append(spinner.el);

///////// End Spinner


trace =[];
trace["activate_task"]=[];
trace["check_preempt_curr"]=[];
trace["clockevents_program_event"]=[];
trace["_cond_resched"]=[];
trace["deactivate_task"]=[];
trace["dput"]=[];
trace["filename_lookup"]=[];
trace["getname_flags"]=[];
trace["hrtimer_cancel"]=[];
trace["hrtimer_try_to_cancel"]=[];
trace["__inode_permission"]=[];
trace["inode_permission"]=[];
trace["kmem_cache_alloc"]=[];
trace["kmem_cache_free"]=[];
trace["legitimize_mnt"]=[];
trace["link_path_walk"]=[];
trace["mntput_no_expire"]=[];
trace["None"]=[];
trace["path_get"]=[];
trace["path_init"]=[];
trace["path_lookupat"]=[];
trace["preempt_schedule_common"]=[];
trace["__remove_hrtimer"]=[];
trace["sched_clock_cpu"]=[];
trace["__schedule"]=[];
trace["__slab_free"]=[];
trace["sys_chdir"]=[];
trace["task_work_add"]=[];
trace["tick_program_event"]=[];
trace["timerqueue_del"]=[];
trace["ttwu_do_wakeup"]=[];
trace["unlazy_walk"]=[];
trace["update_rq_clock"]=[];
trace["user_path_at_empty"]=[];
trace["walk_component"]=[];
trace["activate_task"].push("enqueue_task");
trace["check_preempt_curr"].push("resched_curr");
trace["clockevents_program_event"].push("ktime_get");
trace["_cond_resched"].push("preempt_schedule_common");
trace["deactivate_task"].push("dequeue_task");
trace["dput"].push("lockref_put_return");
trace["filename_lookup"].push("path_lookupat");
trace["filename_lookup"].push("restore_nameidata");
trace["getname_flags"].push("kfree");
trace["getname_flags"].push("kmem_cache_alloc");
trace["getname_flags"].push("kmem_cache_alloc_trace");
trace["getname_flags"].push("kmem_cache_free");
trace["getname_flags"].push("putname");
trace["getname_flags"].push("strncpy_from_user");
trace["hrtimer_cancel"].push("hrtimer_try_to_cancel");
trace["hrtimer_try_to_cancel"].push("_raw_spin_unlock_irqrestore");
trace["hrtimer_try_to_cancel"].push("__remove_hrtimer");
trace["__inode_permission"].push("generic_permission");
trace["inode_permission"].push("__inode_permission");
trace["__inode_permission"].push("security_inode_permission");
trace["kmem_cache_alloc"].push("_cond_resched");
trace["kmem_cache_alloc"].push("memset");
trace["kmem_cache_free"].push("__slab_free");
trace["legitimize_mnt"].push("__legitimize_mnt");
trace["legitimize_mnt"].push("mntput_no_expire");
trace["link_path_walk"].push("dput");
trace["link_path_walk"].push("mntput");
trace["link_path_walk"].push("unlazy_walk");
trace["mntput_no_expire"].push("task_work_add");
trace["None"].push("sys_chdir");
trace["path_get"].push("lockref_get");
trace["path_get"].push("mntget");
trace["path_init"].push("fput");
trace["path_init"].push("path_get");
trace["path_init"].push("set_root_rcu");
trace["path_lookupat"].push("complete_walk");
trace["path_lookupat"].push("link_path_walk");
trace["path_lookupat"].push("path_init");
trace["path_lookupat"].push("terminate_walk");
trace["path_lookupat"].push("walk_component");
trace["preempt_schedule_common"].push("__schedule");
trace["__remove_hrtimer"].push("__hrtimer_get_next_event");
trace["__remove_hrtimer"].push("tick_program_event");
trace["__remove_hrtimer"].push("timerqueue_del");
trace["sched_clock_cpu"].push("sched_clock");
trace["__schedule"].push("activate_task");
trace["__schedule"].push("deactivate_task");
trace["__schedule"].push("finish_task_switch");
trace["__schedule"].push("hrtimer_active");
trace["__schedule"].push("hrtimer_cancel");
trace["__schedule"].push("_raw_spin_lock");
trace["__schedule"].push("_raw_spin_lock_irq");
trace["__schedule"].push("rcu_note_context_switch");
trace["__schedule"].push("__switch_to");
trace["__schedule"].push("ttwu_do_wakeup");
trace["__schedule"].push("ttwu_stat");
trace["__schedule"].push("update_rq_clock");
trace["__slab_free"].push("cmpxchg_double_slab");
trace["__slab_free"].push("_raw_spin_lock_irqsave");
trace["sys_chdir"].push("inode_permission");
trace["sys_chdir"].push("path_put");
trace["sys_chdir"].push("set_fs_pwd");
trace["sys_chdir"].push("user_path_at_empty");
trace["task_work_add"].push("kick_process");
trace["tick_program_event"].push("clockevents_program_event");
trace["timerqueue_del"].push("rb_erase");
trace["timerqueue_del"].push("rb_next");
trace["ttwu_do_wakeup"].push("check_preempt_curr");
trace["unlazy_walk"].push("drop_links");
trace["unlazy_walk"].push("legitimize_mnt");
trace["unlazy_walk"].push("lockref_get_not_dead");
trace["update_rq_clock"].push("sched_clock_cpu");
trace["user_path_at_empty"].push("filename_lookup");
trace["user_path_at_empty"].push("getname_flags");
trace["walk_component"].push("mutex_lock");
trace["walk_component"].push("mutex_unlock");





var depth = 1;
var node_depth = 100;
var node_height = 20;

var m = [20, 120, 20, 120],
    w = 80000 - m[1] - m[3],
    h = 80000 - m[0] - m[2],
    i = 0;

var tree; // = d3.layout.tree() .size([h, w]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) {
        return [d.y, d.x];
    });

var vis = d3.select("#tree").append("svg:svg")
    .attr("width", w + m[1] + m[3])
    .attr("height", h + m[0] + m[2])
    .attr("id", "treesvg")
    .style("overflow", "auto")
    .append("svg:g")
    .attr("transform", "translate(" + m[3] + "," + m[0] + ")");


var gdict = [];

// nodenames to be excluded
var omit_list = ['__fentry__', '#','__stack_chk_fail'];

function omit(node) {
    omit_list.forEach(function(f) {
        if (node.children) {
            filtered = [];
            node.children.forEach(function(c) {
                if (c.label != f) {
                    filtered.push(c);
                }
            });
            node.children = filtered;
        }
    });
    if (node.children == []) {
        node.children = null;
    }
    return node;
}

function node_to_dict(node) {
    node = omit(node);
    children = node.children ? node.children : []; 

    children.forEach(function(child) {
        if (child.type == "original") {
            node_to_dict(child);
        }
    });
    copy = JSON.parse(JSON.stringify(node));
    copy._children = copy.children;
    copy.children = null;
    gdict[node.name] = copy;
}


function init() {

    $("#loading").show();
    depth = $("input[name='depth']").val();
    depth = parseInt(depth) - 1;
    tree = d3.layout.tree();//
    var json_f = getParameterByName('json') ? getParameterByName('json') : 'sys_chdir.json' ;
    d3.json(json_f, function(error, tree) {

        root = tree;
        // root initialized above with the html
        root.x0 = h / 2;
        root.y0 = 0;

        function toggleAll(d) {
            if (d.children && d.children != []) {
                d.children.forEach(toggleAll);
                toggle(d);
            } else {
                delete d['children'];
                delete d['_children'];
            }
        }

        node_to_dict(root);
        // hide all nodes
        root.children.forEach(toggleAll);
        update(root);
        toggle_to(root,depth);
        goto_node(root);
    });
}

function toggle_to(node,depth){
    if (depth <= 0 ){ // || node.type != "original"){
        return;
    }
    children = node.children ? node.children : node._children;
    if ( ! children ){
        return;
    }
    children.forEach(function(c){
        toggle(c);
        update(c);
        toggle_to(c,depth - 1);
    });
}

function goto_node(node){
    w = window.innerWidth ;
    h = window.innerHeight / 2;
    window.scrollTo(node.y , node.x - h);
}

function resize(direction, pm) {
    size = tree.size();
    if (direction == 'x') {
        factor = node_height > 5 ? 3 : 1; 
        node_height += pm == '+' ? factor : -factor;
        node_height = node_height < 2 ? 1 : node_height;
    }
    if (direction == 'y') {
        node_depth += pm == '+' ? 20 : -20
    }
    update(tree);
    goto_node(root);
}


function update(source) {

    function has_children(node) {
        original = gdict[node.label];
        if (original && original._children && original._children.length > 0) {
            return true;
        }
        return false;
    }

    function is_collapsed(node){
        if ( ! has_children(node) ){
            return false;
        }
        original = gdict[node.label];
        return original.children ? false : true ;
    }
            

    function node_color(node) {
        if (node.type == "duplicate" || node.type == "copy") {
            if (node.children){
                return "white";
            }
            if (is_collapsed(node)) {
                return "lightsteelblue";
            } else {
                return "darksalmon";
            }
        }
        if (node._children && has_children(node) ) {
            return "lightsteelblue";
        }
        return "white";
    }

    // Check if a link is in the trace array
    function is_traced(link){
        source = link.source;
        target = link.target;
        traced = false;
        trace_source = trace[source.label];
        if( !trace_source || ! target ){
            return traced;
        }
        trace_source.forEach(function(trace_dest){
            if (trace_dest == target.label){
                traced = true;
             }
        });
        return traced;
    }

    function get_link_class(link){
        pclass = "link";
        if(is_traced(link)){
            pclass += " trace";
        }
        return pclass;
    }

    var duration = d3.event && d3.event.altKey ? 5000 : 500;

    // compute the new height
    var levelWidth = [1];
    var childCount = function(level, n) {

        if (n.children && n.children.length > 0) {
            if (levelWidth.length <= level + 1) levelWidth.push(0);

            if (level > depth) {
                depth = level;
            }
            levelWidth[level + 1] += n.children.length + level * 1.5;
            n.children.forEach(function(d) {
                childCount(level + 1, d);
            });
        }
    };
    childCount(0, root);

    // Compute the new tree layout.
    var newHeight = d3.max(levelWidth) * node_height; // 20 pixels per line

    if(! tree.cust_size){
        tree = tree.size([newHeight, depth * 10]);
    }

    var nodes = tree.nodes(root).reverse();

    if(! tree.cust_size){
        nodes.forEach(function(d) {
            d.y = d.depth * node_depth;
        });
    }

    tree.cust_size = false;

    // Update the nodes.
    var node = vis.selectAll("g.node")
        .data(nodes, function(d) {
            return d.id || (d.id = ++i);
        });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("svg:g")
        .attr("class", "node")
        .attr("transform", function(d) {
            return "translate(" + source.y0 + "," + source.x0 + ")";
        })
        .on("click", function(d) {
            toggle(d);
            update(d);
            //console.log(d);
            //goto_node(d);
        });

    nodeEnter.append("svg:circle")
        .attr("r", 1e-6)
        .style("fill", node_color);

    nodeEnter.append("svg:text")
        .attr("x", function(d) {
            return has_children(d) ? -10 : 10;
        })
        .attr("dy", ".35em")
        .attr("text-anchor", function(d) {
            return has_children(d) ? "end" : "start";
        })
        .text(function(d) {
            return d.label;
        })
        .style("fill-opacity", 1e-6);

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function(d) {
            return "translate(" + d.y + "," + d.x + ")";
        });

    nodeUpdate.select("circle")
        .attr("r", 4.5)
        .style("fill", node_color);

    nodeUpdate.select("text")
        .style("fill-opacity", 1);

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function(d) {
            return "translate(" + source.y + "," + source.x + ")";
        })
        .remove();

    nodeExit.select("circle")
        .attr("r", 1e-6);

    nodeExit.select("text")
        .style("fill-opacity", 1e-6);

    // Update the links.
    var link = vis.selectAll("path.link")
        .data(tree.links(nodes), function(d) {
            return d.target.id;
        });

    // Enter any new links at the parent's previous position.
    link.enter().insert("svg:path", "g")
        .attr("class", get_link_class)
        //.attr("class", "link")
        .attr("d", function(d) {
            var o = {
                x: source.x0,
                y: source.y0
            };
            return diagonal({
                source: o,
                target: o
            });
        })
        .transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(duration)
        .attr("d", function(d) {
            var o = {
                x: source.x,
                y: source.y
            };
            return diagonal({
                source: o,
                target: o
            });
        })
        .remove();

    // Stash the old positions for transition.
    nodes.forEach(function(d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
    $("#loading").hide();
}


// Toggle children.
function toggle(d) {

    function set_dup(node) {
        node.type = 'duplicate';
        node._children = node.children;
        node.children = null;
    }

    function copy_original(node) {
        if (node.type == 'duplicate') {
            original = gdict[node.label];
            node.type = "copy";
            if (!original || !original._children) {
                console.log('ERR: NO ORIGINAL');
                console.log(node);
                return;
            }
            children = JSON.parse(JSON.stringify(original._children));
            children.forEach(set_dup);
            node.x_children = children == [] ? null : children;
        }
    }

    if (d.type == "duplicate") {
        copy_original(d);
        d.children = d.x_children;
    } else if (d.children) {
        d._children = d.children;
        d.children = null;
    } else {
        d.children = d._children;
        d._children = null;
    }
}

function get_ancestors(node, chain) {
    console.log(node.parent);
    if (node.parent){
        chain.push(node.parent);
        get_ancestors(node.parent,chain);
    }
}


// Retrieve url parameter values
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

init();
//$("#control").draggable();

// Cause enter on the depth to expand
$("#depth").keyup(function(event){
    if(event.keyCode == 13){
        $("#expand").click();
    }
});


