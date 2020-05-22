#!/usr/bin/env python3
import os


def gen_controllers(end=1, start=1):
    base_path = "gen/controllers"
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    for n in range(start, end + 1):
        content = f"""import {{ Context }} from "https://deno.land/x/oak/mod.ts";
import {{Service{n}, Service{n}Factory}} from "../../services/service{n}/service{n}.ts";

export default async (context:Context) => {{
    const service: Service{n} = Service{n}Factory(1, "2", 3, "4");
    console.assert(service.service1Type3.e.a === 1)
    console.assert(service.service1Type3.f.d === "4")
	context.response.body = "Route {n} response";
}};
"""
        controller_path = os.path.join(base_path, f"route{n}")
        if not os.path.exists(controller_path):
            try:
                os.mkdir(controller_path)
            except OSError:
                print("Failed to create directory")
                return
        filename = f"route{n}Controller.ts"
        f = open(os.path.join(controller_path, filename), "w")
        print(content, file=f)
        f.close()


def gen_services(end=1, start=1):
    base_path = "gen/services"
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    import_statement = ""
    for n in range(start, end + 1):
        import_statements = []
        import_statements_str = ""
        interface_assignments = []
        interface_assigments_str = ""
        interface_declarations = []
        interface_declarations_str = ""

        if n > start:
            for m in range(start, n):
                import_statements.append(f'import {{ Service{m}Type3, Service{m}Class4 }} from "../service{m}/service{m}.ts"')
                interface_assignments.append(f'\t\tservice{m}Type3: new Service{m}Class4(a, b, c, d),')
                interface_declarations.append(f'\tservice{m}Type3: Service{m}Type3')
            import_statements_str = "\n".join(import_statements)
        else:
            interface_assignments.append(f'\t\tservice{n}Type3: new Service{n}Class4(a, b, c, d),')
            interface_declarations.append(f'\tservice{n}Type3: Service{n}Type3')
        interface_assigments_str = "\n".join(interface_assignments)
        interface_declarations_str = "\n".join(interface_declarations)

        content = f"""
{import_statements_str}

export function Service{n}Factory(a: number, b: string, c: number, d: string): Service{n} {{
	return {{
{interface_assigments_str}
    }}
}};

export interface Service{n} {{
{interface_declarations_str}
}}

export interface Service{n}Type1 {{
	a: number;
	b: string;
}}

export interface Service{n}Type2 {{
	c: number;
	d: string;
}}

export class Service{n}Class1 implements Service{n}Type1 {{
	a: number;
	b: string;
	constructor(a: number, b: string) {{
		this.a = a;
		this.b = b;
	}}
}}

export class Service{n}Class2 implements Service{n}Type2 {{
	c: number;
	d: string;
	constructor(c: number, d: string) {{
		this.c = c;
		this.d = d;
	}}
}}

export interface Service{n}Type3 {{
	e: Service{n}Class1;
	f: Service{n}Class2;
}}

export class Service{n}Class3 implements Service{n}Type3 {{
	e: Service{n}Class1;
	f: Service{n}Class2;
	constructor(e: Service{n}Class1, f: Service{n}Class2) {{
		this.e = e;
		this.f = f;
	}}
}}

export class Service{n}Class4 extends Service{n}Class3 {{
    constructor(a: number, b: string, c: number, d: string) {{
		super(new Service{n}Class1(a, b), new Service{n}Class2(c, d));
	}}
}}
"""
        class_path = os.path.join(base_path, f"service{n}")
        if not os.path.exists(class_path):
            try:
                os.mkdir(class_path)
            except OSError:
                print("Failed to create directory")
                return
        filename = f"service{n}.ts"
        f = open(os.path.join(class_path, filename), "w")
        print(content, file=f)
        f.close()


def gen_router(end=1, start=1, max_complexity=500): 
    imports = ""
    for n in range(start, end + 1):
        imports += f'import route{n}Controller from "./controllers/route{n}/route{n}Controller.ts";\n'
    
    router_statements = []
    for n in range(start, end, min(max_complexity, end + 1)):
        gets = ""
        e = n + min(max_complexity, end - n + 1)
        for i in range(n, e):
            gets += f'\n\t.get("/route{i}", route{i}Controller)'
        router_statements.append(f"\n// routes {n} - {e-1} (defs are split to avoid compilation errs)\nrouter{gets};")
        
    router_statements_str = "\n".join(router_statements)

    content = f"""import {{ Router }} from "https://deno.land/x/oak/mod.ts";

{imports}

const router = new Router();

{router_statements_str}

export default router;
"""
    f = open("gen/router.ts", "w")
    print(content, file=f)
    f.close()


if __name__ == "__main__":
    s = 1
    e = 500
    gen_controllers(end=e, start=s)
    gen_router(end=e,start=s)
    gen_services(end=e,start=s)