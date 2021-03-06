parallel_nodes(['linux && cura', 'windows && cura']) {
    // Prepare building
    stage('Prepare') {
        // Ensure we start with a clean build directory.
        step([$class: 'WsCleanup'])

        // Checkout whatever sources are linked to this pipeline.
        checkout scm
    }

    // If any error occurs during building, we want to catch it and continue with the "finale" stage.
    catchError {
        // Building and testing should happen in a subdirectory.
        dir('build') {
            // Perform the "build". Since Uranium is Python code, this basically only ensures CMake is setup.
            stage('Build') {
                def branch = env.BRANCH_NAME
                if(!(branch =~ /^2.\d+$/)) {
                    branch = "master"
                }

                // Ensure CMake is setup. Note that since this is Python code we do not really "build" it.
                cmake '..', "-DCMAKE_PREFIX_PATH=${env.CURA_ENVIRONMENT_PATH}/${branch} -DCMAKE_BUILD_TYPE=Release"
            }

            // Try and run the unit tests. If this stage fails, we consider the build to be "unstable".
            stage('Unit Test') {
                try {
                    make 'test'
                } catch(e) {
                    currentBuild.result = "UNSTABLE"
                }
            }

            // Perform pylint checks on the source code. If this step fails, we do not consider it an error.
            stage('Lint') {
                try {
                    if(isUnix()) {
                        // "Check" target currently does not work on Windows
                        sh 'make check'
                    }
                } catch(e) {
                    currentBuild.result = "SUCCESS"
                }
            }
        }
    }

    // Perform any post-build actions like notification and publishing of unit tests.
    stage('Finalize') {
        // Publish the test results to Jenkins.
        junit allowEmptyResults: true, testResults: 'build/junit*.xml'

        // Publish the pylint results to Jenkins.
        if(isUnix()) {
            step([
                $class: 'WarningsPublisher',
                parserConfigurations: [[parserName: 'PyLint', pattern: 'build/pylint.log']],
            ])
        }

        // Send notifications about the build result
        notify_build_result(env.CURA_EMAIL_RECIPIENTS, '#cura-dev', ['master', '2.'])
    }
}
