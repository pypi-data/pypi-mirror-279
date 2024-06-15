import { createContext, createSignal, type Accessor, type Setter } from "solid-js";
import { type Span, type Subject } from "./debugger_client";
import { unwrap } from "solid-js/store";

function simple_eq<T>(a: T, b: T): boolean {
    return a === b;
}

//------------------------------------------------------------------------------
// Selection
//------------------------------------------------------------------------------

export class Selection<T> {
    selected: Accessor<T[]>;
    protected set_selected: Setter<T[]>;

    constructor(public name: string, protected eq: (a: T, b: T) => boolean = simple_eq) {
        [this.selected, this.set_selected] = createSignal<T[]>([]);
    }

    primary(): T|undefined {
        return this.selected()[0];
    }

    last(): T|undefined {
        const cur = this.selected();
        return cur[cur.length - 1];
    }

    is_selected(v: any): boolean {
        for (let sel of this.selected()) {
            if (this.eq(sel, v)) return true;
        }
        return false;
    }

    clear = () => this.set_selected([]);

    select = (v: T) => this.set_selected([v]);

    add = (v: T) => {
        if (this.is_selected(v)) return;
        const cur = this.selected();
        this.set_selected([...cur, v]);
        return this;
    }

    remove = (v: T) => {
        const cur = this.selected();
        for(let ix = 0; ix < cur.length; ix += 1) {
            if(this.eq(cur[ix], v)) {
                this.set_selected(cur.toSpliced(ix, 1));
                break;
            }
        }
        return this;
    }

    toggle = (v: T, on = !this.is_selected(v)) => {
        if(on) return this.add(v)
        return this.remove(v)
    }
}

export function createSelectionContext<T>(name: string, eq?: (a: T, b: T) => boolean) {
    return createContext(new Selection<T>(name, eq));
}

//------------------------------------------------------------------------------
// Global selection pools
//------------------------------------------------------------------------------

export const EventListSelection = createSelectionContext<Subject>("EventList");
export const EventDetailSelection = createSelectionContext<Subject>("EventDetail");
