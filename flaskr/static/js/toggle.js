/**
 * Created by jiayun.wei on 6/16/16.
 */
function toggle(crtid) {
    theObj=document.getElementById(crtid).style;
    if (theObj.display=="none")
        theObj.display="block";
    else
        theObj.display="none";
}
function togglefollowers() {
    theObj=document.getElementById('expandfollowers').style;
    if (theObj.display=="none")
        theObj.display="block";
    else
        theObj.display="none";
}
