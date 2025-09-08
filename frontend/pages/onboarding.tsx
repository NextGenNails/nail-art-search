import Head from 'next/head'
import Link from 'next/link'

export default function Onboarding() {
  return (
    <>
      <Head>
        <title>Nail&apos;d Early Onboarding</title>
        <meta name="description" content="Join Nail'd as a featured nail tech" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen" style={{ backgroundColor: '#F5F5F0' }}>
        {/* Navigation */}
        <nav className="pt-8 px-6 sm:px-12 md:px-16 lg:px-24">
          <Link href="/" className="text-black hover:text-gray-600 transition-colors pp-eiko text-lg">
            ← Back to Home
          </Link>
        </nav>

        <div className="container mx-auto px-6 sm:px-12 md:px-16 lg:px-24 pt-12 pb-24">
          {/* Header */}
          <div className="max-w-4xl mx-auto text-left mb-16">
            <h1 className="text-6xl sm:text-7xl md:text-8xl font-medium text-black mb-4 pp-eiko leading-tight">
              Nail&apos;d Early<br />
              Onboarding
            </h1>
          </div>

          {/* Main Content */}
          <div className="max-w-4xl mx-auto">
            {/* You Do Fire Nails Section */}
            <div className="text-center mb-16">
              <h2 className="text-3xl sm:text-4xl font-medium text-black mb-8 pp-eiko">
                You Do Fire Nails. We Bring the Clients.
              </h2>
              
              <div className="w-24 h-px bg-black mx-auto mb-8"></div>
              
              <div className="mb-12">
                <h3 className="text-2xl font-medium text-black mb-6 pp-eiko">
                  What is Nail&apos;d?
                </h3>
                <p className="text-base leading-relaxed text-black max-w-3xl mx-auto font-inter">
                  Nail&apos;d connects nail techs and salons with local clients—and we do it based on style, not reviews or price. 
                  Our platform puts your designs front and center. Clients upload photos of the nails they want, and we 
                  match them to techs who bring that vision to life. We hype your work, build your brand, and send you 
                  clients who love your artistry.
                </p>
              </div>
            </div>

            {/* What You Get Section */}
            <div className="text-center mb-16">
              <h3 className="text-2xl font-medium text-black mb-8 pp-eiko">
                What You Get:
              </h3>
              
              <div className="space-y-4 max-w-2xl mx-auto">
                <p className="text-base text-black font-inter">A free personal profile to showcase your best sets</p>
                <p className="text-base text-black font-inter">Local marketing—without lifting a finger</p>
                <p className="text-base text-black font-inter">100% of what you charge (we don&apos;t take a cut!)</p>
                <p className="text-base text-black font-inter">Bookings from clients who know your style already</p>
                <p className="text-base text-black font-inter">Featured on our TikTok & IG with 101K+ reach</p>
              </div>
              
              <p className="text-sm text-black mt-8 font-inter italic">
                You&apos;re always in control. Set your services, prices, and schedule. We just bring more heat to your business.
              </p>
            </div>

            {/* Who It's For Section */}
            <div className="text-center mb-16">
              <h3 className="text-2xl font-medium text-black mb-8 pp-eiko">
                Who It&apos;s For?
              </h3>
              
              <div className="space-y-4 max-w-2xl mx-auto">
                <p className="text-base text-black font-inter">Salon techs ready to grow their client list</p>
                <p className="text-base text-black font-inter">Independent techs building a name</p>
                <p className="text-base text-black font-inter">
                  Anyone who does 
                  <span className="inline-block mx-1">
                    <span className="text-yellow-600">🔥</span>
                  </span>
                  nails and wants to get booked—not ghosted
                </p>
              </div>
            </div>

            {/* Let Us Work For You Section */}
            <div className="text-center mb-16">
              <h3 className="text-2xl font-medium text-black mb-8 pp-eiko">
                Let Us Work For You
              </h3>
              
              <div className="space-y-2 max-w-2xl mx-auto mb-8">
                <p className="text-base text-black font-inter font-semibold">Your only job? Do great nails.</p>
                <p className="text-base text-black font-inter">Our job? Drive clients, build your brand, and keep the schedule full.</p>
              </div>
            </div>

            {/* Apply Section */}
            <div className="text-center">
              <h3 className="text-2xl font-medium text-black mb-8 pp-eiko flex items-center justify-center">
                <span className="mr-2">💫</span>
                Apply to Be a Featured Tech:
              </h3>
              
              {/* QR Code Placeholder */}
              <div className="flex justify-center mb-8">
                <div className="w-48 h-48 bg-white border-2 border-black flex items-center justify-center">
                  <div className="w-40 h-40 bg-black"></div>
                </div>
              </div>
              
              <p className="text-sm text-gray-600 font-inter">
                Scan QR code to apply or visit our application form
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
