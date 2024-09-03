/**
 * v0 by Vercel.
 * @see https://v0.dev/t/FHzHw5PkIN8
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
import { Sheet, SheetTrigger, SheetContent } from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { Breadcrumb, BreadcrumbList, BreadcrumbItem, BreadcrumbLink, BreadcrumbSeparator, BreadcrumbPage } from "@/components/ui/breadcrumb"
import { Input } from "@/components/ui/input"
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuItem, DropdownMenuCheckboxItem } from "@/components/ui/dropdown-menu"
import { Card, CardHeader, CardTitle, CardDescription, CardFooter, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table"

export default function Component() {
  return (
    <div className="flex min-h-screen w-full flex-col bg-muted/40">
      <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background px-4 sm:static sm:h-auto sm:border-0 sm:bg-transparent sm:px-6">
        <Sheet>
          <SheetTrigger asChild>
            <Button size="icon" variant="outline" className="sm:hidden">
              <div className="h-5 w-5" />
              <span className="sr-only">Toggle Menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="sm:max-w-xs">
            <nav className="grid gap-6 text-lg font-medium">
              <Link
                href="#"
                className="group flex h-10 w-10 shrink-0 items-center justify-center gap-2 rounded-full bg-primary text-lg font-semibold text-primary-foreground md:text-base"
                prefetch={false}
              >
                <HospitalIcon className="h-5 w-5 transition-all group-hover:scale-110" />
                <span className="sr-only">Hospital Management</span>
              </Link>
              <Link href="#" className="flex items-center gap-4 px-2.5 text-foreground" prefetch={false}>
                <TicketIcon className="h-5 w-5" />
                Queuing
              </Link>
              <Link
                href="#"
                className="flex items-center gap-4 px-2.5 text-muted-foreground hover:text-foreground"
                prefetch={false}
              >
                <BedIcon className="h-5 w-5" />
                Bed Availability
              </Link>
              <Link
                href="#"
                className="flex items-center gap-4 px-2.5 text-muted-foreground hover:text-foreground"
                prefetch={false}
              >
                <HospitalIcon className="h-5 w-5" />
                Patient Admission
              </Link>
              <Link
                href="#"
                className="flex items-center gap-4 px-2.5 text-muted-foreground hover:text-foreground"
                prefetch={false}
              >
                <MedalIcon className="h-5 w-5" />
                Medicine Dispensation
              </Link>
              <Link
                href="#"
                className="flex items-center gap-4 px-2.5 text-muted-foreground hover:text-foreground"
                prefetch={false}
              >
                <WarehouseIcon className="h-5 w-5" />
                Inventory Management
              </Link>
            </nav>
          </SheetContent>
        </Sheet>
        <Breadcrumb className="hidden md:flex">
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbLink asChild>
                <Link href="#" prefetch={false}>
                  Hospital Management
                </Link>
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbPage>Overview</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
        <div className="relative ml-auto flex-1 md:grow-0">
          <div className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search..."
            className="w-full rounded-lg bg-background pl-8 md:w-[200px] lg:w-[336px]"
          />
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" size="icon" className="overflow-hidden rounded-full">
              <img
                src="/placeholder.svg"
                width={36}
                height={36}
                alt="Avatar"
                className="overflow-hidden rounded-full"
                style={{ aspectRatio: "36/36", objectFit: "cover" }}
              />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem>Settings</DropdownMenuItem>
            <DropdownMenuItem>Support</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem>Logout</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </header>
      <main className="grid flex-1 items-start gap-4 p-4 sm:px-6 sm:py-0 md:gap-8 lg:grid-cols-3 xl:grid-cols-3">
        <div className="grid auto-rows-max items-start gap-4 md:gap-8 lg:col-span-2">
          <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-2 xl:grid-cols-4">
            <Card className="sm:col-span-2" x-chunk="dashboard-05-chunk-0">
              <CardHeader className="pb-3">
                <CardTitle>Queuing Management</CardTitle>
                <CardDescription className="max-w-lg text-balance leading-relaxed">
                  Streamline patient flow and reduce wait times with our advanced queuing system.
                </CardDescription>
              </CardHeader>
              <CardFooter>
                <Button>Manage Queues</Button>
              </CardFooter>
            </Card>
            <Card x-chunk="dashboard-05-chunk-1">
              <CardHeader className="pb-2">
                <CardDescription>Bed Occupancy</CardDescription>
                <CardTitle className="text-4xl">85%</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-xs text-muted-foreground">+5% from last week</div>
              </CardContent>
              <CardFooter>
                <Progress value={85} aria-label="85% bed occupancy" />
              </CardFooter>
            </Card>
            <Card x-chunk="dashboard-05-chunk-2">
              <CardHeader className="pb-2">
                <CardDescription>Admissions This Month</CardDescription>
                <CardTitle className="text-4xl">1,329</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-xs text-muted-foreground">+10% from last month</div>
              </CardContent>
              <CardFooter>
                <Progress value={12} aria-label="12% increase in admissions" />
              </CardFooter>
            </Card>
            <Card x-chunk="dashboard-05-chunk-3">
              <CardHeader className="pb-2">
                <CardDescription>Medicine Dispensed</CardDescription>
                <CardTitle className="text-4xl">5,329</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-xs text-muted-foreground">+15% from last month</div>
              </CardContent>
              <CardFooter>
                <Progress value={15} aria-label="15% increase in medicine dispensed" />
              </CardFooter>
            </Card>
          </div>
          <Tabs defaultValue="overview">
            <div className="flex items-center">
              <TabsList>
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="queuing">Queuing</TabsTrigger>
                <TabsTrigger value="beds">Bed Availability</TabsTrigger>
                <TabsTrigger value="admissions">Patient Admissions</TabsTrigger>
                <TabsTrigger value="medicine">Medicine Dispensation</TabsTrigger>
                <TabsTrigger value="inventory">Inventory Management</TabsTrigger>
              </TabsList>
              <div className="ml-auto flex items-center gap-2">
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="outline" size="sm" className="h-7 gap-1 text-sm">
                      <FilterIcon className="h-3.5 w-3.5" />
                      <span className="sr-only sm:not-sr-only">Filter</span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Filter by</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuCheckboxItem checked>Delhi</DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem>Noida</DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem>Gurgaon</DropdownMenuCheckboxItem>
                  </DropdownMenuContent>
                </DropdownMenu>
                <Button size="sm" variant="outline" className="h-7 gap-1 text-sm">
                  <ImportIcon className="h-3.5 w-3.5" />
                  <span className="sr-only sm:not-sr-only">Export</span>
                </Button>
              </div>
            </div>
            <TabsContent value="overview">
              <Card x-chunk="dashboard-05-chunk-4">
                <CardHeader className="px-7">
                  <CardTitle>Hospital Overview</CardTitle>
                  <CardDescription>Key metrics for the hospital network.</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-8">
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                      <div className="bg-accent p-6 rounded-lg">
                        <div className="text-4xl font-bold">85%</div>
                        <div className="text-muted-foreground">Bed Occupancy</div>
                      </div>
                      <div className="bg-accent p-6 rounded-lg">
                        <div className="text-4xl font-bold">1,329</div>
                        <div className="text-muted-foreground">Admissions This Month</div>
                      </div>
                      <div className="bg-accent p-6 rounded-lg">
                        <div className="text-4xl font-bold">5,329</div>
                        <div className="text-muted-foreground">Medicine Dispensed</div>
                      </div>
                      <div className="bg-accent p-6 rounded-lg">
                        <div className="text-4xl font-bold">92%</div>
                        <div className="text-muted-foreground">Inventory Availability</div>
                      </div>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4">
                      <Card>
                        <CardHeader className="pb-3">
                          <CardTitle>Queuing Performance</CardTitle>
                          <CardDescription>Average wait times and queue lengths.</CardDescription>
                        </CardHeader>
                        <CardContent>
                          <div className="grid gap-4">
                            <div className="flex justify-between">
                              <div>Emergency</div>
                              <div className="font-medium">15 min</div>
                            </div>
                            <div className="flex justify-between">
                              <div>Outpatient</div>
                              <div className="font-medium">45 min</div>
                            </div>
                            <div className="flex justify-between">
                              <div>Pharmacy</div>
                              <div className="font-medium">20 min</div>
                            </div>
                            <div className="flex justify-between">
                              <div>Lab</div>
                              <div className="font-medium">30 min</div>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardHeader className="pb-3">
                          <CardTitle>Inventory Status</CardTitle>
                          <CardDescription>Current stock levels and consumption trends.</CardDescription>
                        </CardHeader>
                        <CardContent>
                          <div className="grid gap-4">
                            <div className="flex justify-between">
                              <div>Surgical Masks</div>
                              <div className="font-medium">15,000</div>
                            </div>
                            <div className="flex justify-between">
                              <div>Paracetamol</div>
                              <div className="font-medium">5,000</div>
                            </div>
                            <div className="flex justify-between">
                              <div>Bandages</div>
                              <div className="font-medium">8,000</div>
                            </div>
                            <div className="flex justify-between">
                              <div>Syringes</div>
                              <div className="font-medium">12,000</div>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="queuing">
              <Card x-chunk="dashboard-05-chunk-5">
                <CardHeader className="px-7">
                  <CardTitle>Queuing Management</CardTitle>
                  <CardDescription>Monitor and optimize patient flow.</CardDescription>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Department</TableHead>
                        <TableHead>Current Queue</TableHead>
                        <TableHead>Average Wait Time</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      <TableRow>
                        <TableCell>Emergency</TableCell>
                        <TableCell>15</TableCell>
                        <TableCell>15 min</TableCell>
                        <TableCell>
                          <Button size="sm" variant="outline">
                            Manage Queue
                          </Button>
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Outpatient</TableCell>
                        <TableCell>45</TableCell>
                        <TableCell>45 min</TableCell>
                        <TableCell>
                          <Button size="sm" variant="outline">
                            Manage Queue
                          </Button>
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Pharmacy</TableCell>
                        <TableCell>20</TableCell>
                        <TableCell>20 min</TableCell>
                        <TableCell>
                          <Button size="sm" variant="outline">
                            Manage Queue
                          </Button>
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Lab</TableCell>
                        <TableCell>30</TableCell>
                        <TableCell>30 min</TableCell>
                        <TableCell>
                          <Button size="sm" variant="outline">
                            Manage Queue
                          </Button>
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="beds">
              <Card x-chunk="dashboard-05-chunk-6">
                <CardHeader className="px-7">
                  <CardTitle>Bed Availability</CardTitle>
                </CardHeader>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  )
}

function BedIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M2 4v16" />
      <path d="M2 8h18a2 2 0 0 1 2 2v10" />
      <path d="M2 17h20" />
      <path d="M6 8v9" />
    </svg>
  )
}


function FilterIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
    </svg>
  )
}


function HospitalIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12 6v4" />
      <path d="M14 14h-4" />
      <path d="M14 18h-4" />
      <path d="M14 8h-4" />
      <path d="M18 12h2a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2h2" />
      <path d="M18 22V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v18" />
    </svg>
  )
}


function ImportIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12 3v12" />
      <path d="m8 11 4 4 4-4" />
      <path d="M8 5H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-4" />
    </svg>
  )
}


function MedalIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M7.21 15 2.66 7.14a2 2 0 0 1 .13-2.2L4.4 2.8A2 2 0 0 1 6 2h12a2 2 0 0 1 1.6.8l1.6 2.14a2 2 0 0 1 .14 2.2L16.79 15" />
      <path d="M11 12 5.12 2.2" />
      <path d="m13 12 5.88-9.8" />
      <path d="M8 7h8" />
      <circle cx="12" cy="17" r="5" />
      <path d="M12 18v-2h-.5" />
    </svg>
  )
}


function TicketIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z" />
      <path d="M13 5v2" />
      <path d="M13 17v2" />
      <path d="M13 11v2" />
    </svg>
  )
}


function WarehouseIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M22 8.35V20a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8.35A2 2 0 0 1 3.26 6.5l8-3.2a2 2 0 0 1 1.48 0l8 3.2A2 2 0 0 1 22 8.35Z" />
      <path d="M6 18h12" />
      <path d="M6 14h12" />
      <rect width="12" height="12" x="6" y="10" />
    </svg>
  )
}