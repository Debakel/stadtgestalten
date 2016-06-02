import { component } from "./util/dom";
import date from "./components/date";
import editor from "./components/editor";
import time from "./components/time";
import user_content from "./components/user-content";

// initialize components on load
component("date", date);
component("editor", editor);
component("time", time);
component("user-content", user_content);