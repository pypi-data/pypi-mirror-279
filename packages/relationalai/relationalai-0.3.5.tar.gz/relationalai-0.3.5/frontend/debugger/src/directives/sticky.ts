import { createEffect, onCleanup } from "solid-js";

// @NOTE: requires the top: -1px trick to cause an intersection.
export function sticky(elem: HTMLElement, pinned_class: () => string) {
    createEffect(() => {
        const klass = pinned_class();
        const observer = new IntersectionObserver(
            ([e]) => e.target.classList.toggle(klass, e.intersectionRatio < 1),
            { threshold: [1] }
        );

        observer.observe(elem);
        onCleanup(() => {
            elem?.classList.toggle(klass)
            observer.disconnect();
        })
    })
}

export default sticky;
